from sys import stdin
from collections import deque


N, M = map(int, stdin.readline().split())
in_degrees = [0] * (N + 1)
adj_list = [set() for _ in range(N + 1)]

for _ in range(M):
    count, *numbers = [int(x) for x in stdin.readline().split()]

    for start in range(count - 1):
        num1 = numbers[start]

        for end in range(start + 1, count):
            num2 = numbers[end]
            if num2 not in adj_list[num1]:
                adj_list[num1].add(num2)
                in_degrees[num2] += 1

result = []
queue = deque()

for idx in range(1, N + 1):
    if not in_degrees[idx]:
        queue.append(idx)

while queue:
    current = queue.popleft()
    result.append(current)

    for node in adj_list[current]:
        in_degrees[node] -= 1

        if not in_degrees[node]:
            queue.append(node)

if len(result) < N:
    print(0)
else:
    for node in result:
        print(node)
