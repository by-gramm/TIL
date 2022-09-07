from sys import stdin
from collections import deque


T = int(stdin.readline())

for _ in range(T):
    K, M, P = map(int, stdin.readline().split())
    in_degrees = [0] * (M + 1)
    adj_list = [set() for _ in range(M + 1)]
    strahlers = [[] for _ in range(M + 1)]

    for _ in range(P):
        A, B = map(int, stdin.readline().split())
        adj_list[A].add(B)
        in_degrees[B] += 1

    queue = deque()

    for node in range(1, M + 1):
        if not in_degrees[node]:
            queue.append(node)
            strahlers[node] = [1, 0]

    while queue:
        current = queue.popleft()

        for node in adj_list[current]:
            in_degrees[node] -= 1

            if not strahlers[node] or (strahlers[node][0] < strahlers[current][0]):
                strahlers[node] = [strahlers[current][0], 1]
            elif strahlers[node][0] == strahlers[current][0]:
                strahlers[node][1] += 1

            if not in_degrees[node]:
                if strahlers[node][1] > 1:
                    strahlers[node] = [strahlers[node][0] + 1, 0]

                queue.append(node)

    print(K, strahlers[-1][0])
