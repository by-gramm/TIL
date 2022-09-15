from sys import stdin
from heapq import heappush, heappop


def get_distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


N = int(stdin.readline())
stars = []
heap = []
visited = [False] * N
groups = [-1] * N

for _ in range(N):
    x, y = map(float, stdin.readline().split())
    stars.append([x, y])

# 각 별들 사이의 거리를 구한다.
for idx1 in range(N - 1):
    for idx2 in range(idx1 + 1, N):
        distance = get_distance(*stars[idx1], *stars[idx2])
        heappush(heap, [distance, idx1, idx2])

total_count, total_distance = 0, 0

while total_count < N - 1:
    distance, num1, num2 = heappop(heap)

    if groups[num1] == groups[num2] and groups[num1] != -1:
        continue

    total_count += 1
    total_distance += distance

    if groups[num1] == -1:
        if groups[num2] == -1:
            groups[num1] = groups[num2] = num1
        else:
            groups[num1] = groups[num2]
    else:
        if groups[num2] == -1:
            groups[num2] = groups[num1]
        else:
            changed_num = groups[num2]

            for idx in range(N):
                if groups[idx] == changed_num:
                    groups[idx] = groups[num1]

    visited[num1] = True
    visited[num2] = True

print(round(total_distance, 2))
