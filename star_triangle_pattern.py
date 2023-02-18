# Problem: Star triangle with a list comprehension
# Print a right triangle of stars (1 to 4 stars per line) using a list
# comprehension with print as the side effect.
# Context: University tutorial / practice exercise, Python
x = [print("*" * i) for i in range(1, 5)]
