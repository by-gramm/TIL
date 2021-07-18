출처: 백준 온라인 저지
https://www.acmicpc.net/problem/2178

<br>

___

### ⏰ 시간 초과 풀이

```python

from sys import stdin
from math import inf


n, m = map(int, stdin.readline().split())

mazes = []

for _ in range(n):
    mazes.append(list(map(int, stdin.readline().rstrip())))

shortest = [[inf] * m for _ in range(n)]
shortest[0][0] = 1


# DFS 알고리즘으로 미로 찾기
def find_path(r, c, end_r, end_c, dist):

    if r < end_r:
        if mazes[r + 1][c] == 1 and dist[r + 1][c] > dist[r][c] + 1:
            dist[r + 1][c] = dist[r][c] + 1
            find_path(r + 1, c, end_r, end_c, dist)

    if c < end_c:
        if mazes[r][c + 1] == 1 and dist[r][c + 1] > dist[r][c] + 1:
            dist[r][c + 1] = dist[r][c] + 1
            find_path(r, c + 1, end_r, end_c, dist)

    if r > 0:
        if mazes[r - 1][c] == 1 and dist[r - 1][c] > dist[r][c] + 1:
            dist[r - 1][c] = dist[r][c] + 1
            find_path(r - 1, c, end_r, end_c, dist)

    if c > 0:
        if mazes[r][c - 1] == 1 and dist[r][c - 1] > dist[r][c] + 1:
            dist[r][c - 1] = dist[r][c] + 1
            find_path(r, c - 1, end_r, end_c, dist)

    return dist[end_r][end_c]


print(find_path(0, 0, n - 1, m - 1, shortest))

```


미로 탐색 알고리즘은 DFS로 구현해야 한다고 어디선가 들어서, DFS 알고리즘으로 구현했다. 재귀 함수로 구현하고, 오류들을 겨우 겨우 고쳐서 제출했는데, 결과는 `런타임 에러(RecursionError)`였다. 

미로 찾기니까 DFS라고 1차원적으로 생각한 것이 문제였다. 이 문제는 단순히 미로의 경로를 구하는 것이 아니라 미로의 최단경로를 구하는 문제고, 최단경로를 구하는 데 적합한 알고리즘은 BFS 알고리즘이다. 중요한 건 '미로'가 아니라 '최단 경로'인데, 미로는 DFS라는 주워들은 말에 꽂힌 것이다.

<br>

#### 최단 경로 알고리즘

- 비가중치 그래프 : `BFS 알고리즘`
- 가중치 그래프 : `다익스트라 알고리즘`

<br>

BFS 알고리즘으로 다시 구현해 보았다. 다행히도 이번에는 <span style="color:green">**맞았습니다!!**</span> 를 보게 되었다.

<br>

### 🔓 정답 풀이

```python

from sys import stdin
from collections import deque


n, m = map(int, stdin.readline().split())

# 지도를 나타내는 2차원 배열
new_maze = []

for _ in range(n):
    # rstrip() 함수로 줄바꿈 문자('\n')를 처리
    new_maze.append([int(x) for x in stdin.readline().rstrip()])

# 최단 거리를 저장하는 2차원 배열
shortest = [[0] * m for _ in range(n)]
# 초기값 설정 : (0, 0)은 자기 자신만을 지나야 하므로 1
shortest[0][0] = 1


# BFS 알고리즘으로 미로 찾기
def get_distance(maze, end_r, end_c, dist):
    queue = deque()
    queue.append((0, 0))

    dist[0][0] = 1

    # 더 이상 탐색할 칸이 없을 때까지 너비 우선 탐색
    while queue:
        r, c = queue.popleft()

        # 맨 아래쪽 줄이 아니라면
        if r < end_r:
            if maze[r + 1][c] == 1 and dist[r + 1][c] == 0:
                dist[r + 1][c] = dist[r][c] + 1
                queue.append((r + 1, c))

        # 맨 오른쪽 줄이 아니라면
        if c < end_c:
            if maze[r][c + 1] == 1 and dist[r][c + 1] == 0:
                dist[r][c + 1] = dist[r][c] + 1
                queue.append((r, c + 1))

        # 맨 위쪽 줄이 아니라면
        if r > 0:
            if maze[r - 1][c] == 1 and dist[r - 1][c] == 0:
                dist[r - 1][c] = dist[r][c] + 1
                queue.append((r - 1, c))

        # 맨 왼쪽 줄이 아니라면
        if c > 0:
            if maze[r][c - 1] == 1 and dist[r][c - 1] == 0:
                dist[r][c - 1] = dist[r][c] + 1
                queue.append((r, c - 1))

    return dist[end_r][end_c]


distance = get_distance(new_maze, n - 1, m - 1, shortest)
print(distance)

```