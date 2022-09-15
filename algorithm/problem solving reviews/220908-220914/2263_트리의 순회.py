from sys import stdin
from collections import deque


N = int(stdin.readline())
inorders = [0] + [int(x) for x in stdin.readline().split()]
postorders = [0] + [int(x) for x in stdin.readline().split()]
root = postorders[N]

reversed_inorders = [0] * (N + 1)

for idx, node in enumerate(inorders):
    reversed_inorders[node] = idx

stack = deque()
stack.append([1, N, 0])

while stack:
    start, end, idx = stack.pop()

    if start > end:
        continue

    sub_root = postorders[end - idx]
    print(sub_root, end=" ")

    # 단말 노드인 경우
    if start == end:
        continue

    sub_root_idx = reversed_inorders[sub_root]
    stack.append([sub_root_idx + 1, end, idx + 1])
    stack.append([start, sub_root_idx - 1, idx])
