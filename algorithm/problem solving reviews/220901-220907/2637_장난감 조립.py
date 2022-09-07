from sys import stdin
from collections import deque


N = int(stdin.readline())
M = int(stdin.readline())

in_degrees = [0] * (N + 1)
needed_parts = [[] for _ in range(N + 1)]

for _ in range(M):
    X, Y, K = map(int, stdin.readline().split())
    in_degrees[Y] += 1
    needed_parts[X].append([Y, K])

basic_parts = dict()

for idx in range(1, N):
    if not needed_parts[idx]:
        basic_parts[idx] = 0

queue = deque([[N, 1]])
counts = [0] * (N + 1)
counts[N] = 1

while queue:
    cnt_num, cnt_count = queue.popleft()

    for num, count in needed_parts[cnt_num]:
        counts[num] += (cnt_count * count)
        in_degrees[num] -= 1

        if not in_degrees[num]:
            queue.append([num, counts[num]])

for num in basic_parts:
    print(num, counts[num])
