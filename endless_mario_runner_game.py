# Problem: Endless runner game with pygame
# Mario-inspired endless runner: a pygame window where the player jumps over
# obstacles on a scrolling ground; score and game state are handled with
# dataclasses.
# Context: Personal practice / experiment
# Endless Mario-Inspired Runner

import random
import sys
from dataclasses import dataclass
from typing import Optional

import pygame


pygame.init()

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 560
GROUND_Y = SCREEN_HEIGHT - 90
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Endless Mario Runner")

# Timing helpers
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("arial", 24)

# Colors
WHITE = (240, 240, 240)
SKY = (135, 206, 250)
GROUND = (160, 120, 70)
PLAYER_COLOR = (50, 90, 200)
MUSHROOM_COLOR = (200, 30, 30)
TURTLE_COLOR = (40, 160, 80)
STAR_COLOR = (255, 215, 0)
KNIFE_COLOR = (220, 220, 220)

# Game constants
GRAVITY = 1600  # pixels per second^2
JUMP_SPEED = 720
PLAYER_WIDTH, PLAYER_HEIGHT = 52, 70
OBSTACLE_SPEED = 360
OBSTACLE_INTERVAL = (900, 1500)  # milliseconds
STAR_INTERVAL = (8000, 14000)
STAR_DURATION_MS = 6000
KNIFE_SPEED = 680


@dataclass
class Obstacle:
    rect: pygame.Rect
    kind: str


@dataclass
class Knife:
    rect: pygame.Rect


class Player:
    def __init__(self) -> None:
        self.rect = pygame.Rect(
            140, GROUND_Y - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT
        )
        self._pos_y = float(self.rect.y)
        self.velocity_y = 0.0
        self.star_active_until = 0

    def update(self, dt: float) -> None:
        self.velocity_y += GRAVITY * dt
        self._pos_y += self.velocity_y * dt
        if self._pos_y + PLAYER_HEIGHT >= GROUND_Y:
            self._pos_y = GROUND_Y - PLAYER_HEIGHT
            self.velocity_y = 0.0
        self.rect.y = int(self._pos_y)

    def jump(self) -> None:
        if self.on_ground:
            self.velocity_y = -JUMP_SPEED

    @property
    def on_ground(self) -> bool:
        return abs((self.rect.bottom) - GROUND_Y) < 2

    def activate_star(self) -> None:
        self.star_active_until = pygame.time.get_ticks() + STAR_DURATION_MS

    @property
    def star_active(self) -> bool:
        return pygame.time.get_ticks() < self.star_active_until


def spawn_obstacle() -> Obstacle:
    kind = random.choice(["mushroom", "turtle"])
    if kind == "mushroom":
        rect = pygame.Rect(SCREEN_WIDTH + 40, GROUND_Y - 42, 46, 42)
    else:
        rect = pygame.Rect(SCREEN_WIDTH + 40, GROUND_Y - 55, 60, 55)
    return Obstacle(rect=rect, kind=kind)


def spawn_star() -> pygame.Rect:
    height_variation = random.randint(0, 130)
    rect = pygame.Rect(SCREEN_WIDTH + 40, GROUND_Y - 140 - height_variation, 34, 34)
    return rect


def draw_ground() -> None:
    pygame.draw.rect(
        screen, GROUND, (0, GROUND_Y, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_Y)
    )
    pygame.draw.line(screen, (100, 80, 50), (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 3)


def draw_player(player: Player) -> None:
    pygame.draw.rect(screen, PLAYER_COLOR, player.rect, border_radius=6)


def draw_obstacles(obstacles: list[Obstacle]) -> None:
    for obs in obstacles:
        color = MUSHROOM_COLOR if obs.kind == "mushroom" else TURTLE_COLOR
        pygame.draw.rect(screen, color, obs.rect, border_radius=8)


def draw_knives(knives: list[Knife]) -> None:
    for knife in knives:
        pygame.draw.rect(screen, KNIFE_COLOR, knife.rect, border_radius=3)


def draw_star(star_rect: Optional[pygame.Rect]) -> None:
    if star_rect:
        pygame.draw.rect(screen, STAR_COLOR, star_rect, border_radius=8)


def draw_hud(score: int, player: Player) -> None:
    score_surface = FONT.render(f"Score: {score}", True, (30, 30, 30))
    screen.blit(score_surface, (20, 20))
    if player.star_active:
        msg = FONT.render("Star power! Press K to throw knives", True, (50, 30, 160))
        screen.blit(msg, (20, 54))


def reset_game(
    player: Player, obstacles: list[Obstacle], knives: list[Knife]
) -> tuple[float, int, Optional[pygame.Rect], int, int]:
    player.rect.x = 140
    player.rect.y = GROUND_Y - PLAYER_HEIGHT
    player._pos_y = float(player.rect.y)
    player.velocity_y = 0.0
    player.star_active_until = 0
    obstacles.clear()
    knives.clear()
    now = pygame.time.get_ticks()
    next_obstacle_time = now + random.randint(*OBSTACLE_INTERVAL)
    next_star_time = now + random.randint(*STAR_INTERVAL)
    return 0.0, next_obstacle_time, None, next_star_time, now


def main() -> None:
    player = Player()
    obstacles: list[Obstacle] = []
    knives: list[Knife] = []
    star_rect: Optional[pygame.Rect] = None
    score = 0.0
    startup_time = pygame.time.get_ticks()
    next_obstacle_time = startup_time + random.randint(*OBSTACLE_INTERVAL)
    next_star_time = startup_time + random.randint(*STAR_INTERVAL)
    last_update_time = startup_time
    game_active = True

    while True:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if game_active:
                    if event.key in (pygame.K_SPACE, pygame.K_UP):
                        player.jump()
                    if event.key == pygame.K_k and player.star_active:
                        knife_rect = pygame.Rect(
                            player.rect.right - 10, player.rect.centery - 4, 32, 8
                        )
                        knives.append(Knife(rect=knife_rect))
                else:
                    if event.key == pygame.K_r:
                        (
                            score,
                            next_obstacle_time,
                            star_rect,
                            next_star_time,
                            last_update_time,
                        ) = reset_game(player, obstacles, knives)
                        game_active = True

        if not game_active:
            screen.fill(SKY)
            draw_ground()
            draw_player(player)
            draw_obstacles(obstacles)
            draw_knives(knives)
            draw_star(star_rect)
            draw_hud(int(score), player)
            game_over_text = FONT.render(
                "Game Over - Press R to restart", True, (180, 40, 40)
            )
            screen.blit(
                game_over_text,
                (
                    SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                    SCREEN_HEIGHT // 2,
                ),
            )
            pygame.display.flip()
            continue

        current_time = pygame.time.get_ticks()

        if current_time >= next_obstacle_time:
            obstacles.append(spawn_obstacle())
            next_obstacle_time = current_time + random.randint(*OBSTACLE_INTERVAL)

        if star_rect is None and current_time >= next_star_time:
            star_rect = spawn_star()
            next_star_time = current_time + random.randint(*STAR_INTERVAL)

        player.update(dt)

        for obs in list(obstacles):
            obs.rect.x -= int(OBSTACLE_SPEED * dt)
            if obs.rect.right < 0:
                obstacles.remove(obs)
                score += 4.0

        for knife in list(knives):
            knife.rect.x += int(KNIFE_SPEED * dt)
            if knife.rect.left > SCREEN_WIDTH:
                knives.remove(knife)

        for knife in list(knives):
            for obs in list(obstacles):
                if knife.rect.colliderect(obs.rect):
                    knives.remove(knife)
                    obstacles.remove(obs)
                    score += 12.0
                    break

        if star_rect:
            star_rect.x -= int(OBSTACLE_SPEED * dt)
            if star_rect.right < 0:
                star_rect = None
            elif star_rect.colliderect(player.rect):
                player.activate_star()
                star_rect = None

        for obs in obstacles:
            if obs.rect.colliderect(player.rect):
                game_active = False
                break

        delta_ms = current_time - last_update_time
        passive_rate = 0.005 if player.star_active else 0.003
        score += delta_ms * passive_rate
        last_update_time = current_time

        screen.fill(SKY)
        draw_ground()
        draw_player(player)
        draw_obstacles(obstacles)
        draw_knives(knives)
        draw_star(star_rect)
        draw_hud(int(score), player)

        pygame.display.flip()


if __name__ == "__main__":
    main()
