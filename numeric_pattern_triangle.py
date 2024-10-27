# Problem: Triangle of alternating 0 and 1
# Read n and print a triangle of n lines where each cell is (i + j) % 2,
# giving an alternating 0/1 pattern.
# Context: University tutorial / practice exercise, Python
n = int(input("give me a number "))
for i in range(1, n + 1):
    for j in range(1, i + 1):
        print((i + j) % 2, end=" ")
    print()
