출처: 백준 온라인 저지

https://www.acmicpc.net/problem/16236

<br>

___

## 📃 문제 설명

NxN 크기의 공간에 물고기 M마리와 아기 상어 1마리가 있다.

아기 상어의 처음 크기는 2이며, 자신의 크기와 같은 수의 물고기를 먹으면 크기가 1 증가한다.

아기 상어는 1초에 상하좌우로 1칸 이동할 수 있다.

아기 상어는 자신보다 작은 물고기만 먹을 수 있으며, 자신보다 작거나 같은 물고기가 있는 칸만 지나갈 수 있다. (즉, 자신과 같은 크기의 물고기는 지나갈 수는 있지만 먹을 수는 없다.)

아기 상어가 어디로 이동할지 결정하는 방법은 아래와 같다.

- 먹을 수 있는 물고기가 1마리라면, 그 물고기를 먹으러 간다.
- 먹을 수 있는 물고기가 1마리보다 많다면, 거리가 가장 가까운 물고기를 먹으러 간다.
  - 거리 = 지나야하는 칸의 개수의 최솟값
  - 거리가 같은 물고기가 여러 마리라면, 가장 위에 있으며, 그 중에서도 가장 왼쪽에 있는 물고기를 먹는다.

- 더 이상 먹을 수 있는 물고기가 없다면, 아기 상어는 엄마 상어에게 도움을 요청한다.

아기 상어가 도움 요청 없이 **몇 초 동안** 물고기를 잡아먹을 수 있는지 구한다.

<br>

## ⏰ 시간 초과 풀이

```python
from sys import stdin
from collections import deque


def get_distance(p1, p2, board, N, size):
    """
    p1에 있는 아기 상어가 p2에 가기 위해 지나야 하는 칸의 개수의 최솟값을 구한다.
    Args:
        size: 현재 아기 상어의 크기
    """
    # 상우하좌
    dr = [-1, 0, 1, 0]
    dc = [0, 1, 0, -1]

    distances = [[0] * N for _ in range(N)]

    queue = deque([p1])

    while queue:
        cnt_r, cnt_c = queue.popleft()
        for i in range(4):
            r, c = cnt_r + dr[i], cnt_c + dc[i]
            # 1) 인덱스가 유효하고 2) 아직 방문하지 않았고 3) 방문 가능하다면
            if (0 <= r < N and 0 <= c < N
                    and not distances[r][c]
                    and size >= board[r][c]):
                distances[r][c] = distances[cnt_r][cnt_c] + 1
                # 현재 탐색 위치가 도착 지점인 경우 => 도착 지점까지의 거리를 리턴한다.
                if (r, c) == p2:
                    return distances[r][c]
                queue.append((r, c))
    
    # p1에서 p2로 갈 수 있는 경로가 없다면 0을 리턴한다.
    return 0


N = int(stdin.readline())
board = [[int(x) for x in stdin.readline().split()] for _ in range(N)]

"""
size: 현재 아기 상어의 크기
total: 아기 상어가 물고기를 잡아먹을 수 있는 시간
count: 아기 상어가 현재 크기인 상태에서 먹은 물고기의 수
"""
size = 2
total = 0
count = 0

# 처음 아기상어의 위치를 구한다.
for r in range(N):
    for c in range(N):
        if board[r][c] == 9:
            # shark_point: 현재 아기상어의 위치
            shark_point = (r, c)
            # 이후 탐색을 위해, 아기상어의 처음 위치를 0으로 만들어준다.
            board[r][c] = 0

while True:
    # shortest: 아기 상어가 물고기를 먹기 위해 이동해야 하는 거리의 최솟값
    shortest = 100

    for r in range(N):
        for c in range(N):
            if 0 < board[r][c] < size:
                distance = get_distance(shark_point, (r, c), board, N, size)
                if distance < shortest:
                    shortest = distance
                    destination = (r, c)

    # 더이상 아기 상어가 먹을 수 있는 물고기가 없다면
    if shortest == 100:
        print(total)
        break

    total += shortest
    r, c = destination
    board[r][c] = 0
    shark_point = (r, c)
    count += 1

    # 아기 상어가 자기 크기만큼 물고기를 잡아먹었다면
    if count == size:
        count = 0
        size += 1

```

처음에는 A지점에서 B지점까지의 거리(아기 상어가 이동해야 하는 칸의 수)를 구하는 `get_distance()` 함수를 만들었다. 그리고 아기 상어가 이동할 때마다, 아기 상어가 먹을 수 있는 물고기 중 가장 가까운 물고기를 찾아서, 해당 위치로 이동하도록 했다. 이렇게 구현한 결과, 시간 초과가 떴다.

위 코드가 시간 초과가 뜬 이유는, 중복되는 작업이 많기 때문이다. 위 코드에서는 A지점에서 B지점까지의 거리를 구하려면, BFS 알고리즘을 이용했다. 그런데 BFS 알고리즘을 이용하면, A지점에서 B지점까지의 거리뿐 아니라, A지점에서 특정 거리에 있는 모든 좌표를 구할 수 있다. 따라서 먹을 수 있는 모든 물고기에 대하여 매번 거리를 구할 필요가 없다. 한 번의 순회로 아기 상어의 현재 위치에서 가장 가까이에 있으며 먹을 수도 있는 물고기들의 좌표를 모두 구할 수 있기 때문이다.

<br>

## 🔓 최종 풀이

최종 풀이에서는 아기 상어가 먹을 수 있는 가장 가까운 물고기의 위치를 구하는 `get_closest_fish()` 함수를 구현했다. 일단 가장 가까이에 있으며 먹을 수 있는 물고기들의 좌표를 모두 구한 뒤, 그중 가장 위에 있으며, 그중 가장 왼쪽에 있는 좌표를 구했다. 

```python
from sys import stdin
from collections import deque


def get_closest_fish(point, board, N, size):
    """
    p1에 있는 아기 상어가 먹을 수 있는 가장 가까운 물고기의 위치를 구한다.
    Args:
        point: 아기 상어의 좌표 ((r, c))
        N: 공간의 가로, 세로 길이
        size: 현재 아기 상어의 크기
    Returns:
        아기 상어가 먹을 수 있는 가장 가까운 물고기의 좌표와 거리
        (단, 아기 상어가 먹을 수 있는 물고기가 없다면 ((-1, -1), -1)
    """
    # 상우하좌
    dr = [-1, 0, 1, 0]
    dc = [0, 1, 0, -1]

    distances = [[0] * N for _ in range(N)]
    r, c = point
    queue = deque([(r, c)])
    # min_distance: 물고기까지의 최소 거리
    min_distance = 1000
    points = []

    while queue:
        cnt_r, cnt_c = queue.popleft()
        # 최소 거리보다 먼 곳을 탐색하는 경우 => 탐색 종료
        if distances[cnt_r][cnt_c] >= min_distance:
            break

        for i in range(4):
            r, c = cnt_r + dr[i], cnt_c + dc[i]
            # 인덱스가 유효하고, 아직 방문하지 않은 경우
            if 0 <= r < N and 0 <= c < N and not distances[r][c]:
                # 1) 먹을 수 있는 물고기가 있다면
                if 0 < board[r][c] < size:
                    distances[r][c] = distances[cnt_r][cnt_c] + 1
                    min_distance = distances[r][c]
                    points.append((r, c))
                    queue.append((r, c))

                # 2) 먹을 수 있는 물고기는 없지만 지나갈 수 있다면
                elif board[r][c] in (0, size):
                    distances[r][c] = distances[cnt_r][cnt_c] + 1
                    queue.append((r, c))

    # p1에서 p2로 갈 수 있는 경로가 없다면
    if not points:
        return (-1, -1), -1
    
    # 좌표들을 1) 위에서 아래로 / 2) 왼쪽에서 오른쪽으로 정렬한다.
    points.sort(key=lambda x: x[1])
    points.sort(key=lambda x: x[0])
    board[points[0][0]][points[0][1]] = 0
    return points[0], min_distance


N = int(stdin.readline())
board = [[int(x) for x in stdin.readline().split()] for _ in range(N)]

"""
size: 현재 아기 상어의 크기
total: 아기 상어가 물고기를 잡아먹을 수 있는 시간
count: 아기 상어가 현재 크기인 상태에서 먹은 물고기의 수
"""
size = 2
total = 0
count = 0

# 처음 아기상어의 위치를 구한다.
for r in range(N):
    for c in range(N):
        if board[r][c] == 9:
            # shark_point: 현재 아기상어의 위치
            shark_point = (r, c)
            # 이후 탐색을 위해, 아기상어의 처음 위치를 0으로 만들어준다.
            board[r][c] = 0

while True:
    shark_point, distance = get_closest_fish(shark_point, board, N, size)

    # 더이상 아기 상어가 먹을 수 있는 물고기가 없다면
    if distance == -1:
        print(total)
        break

    total += distance
    count += 1

    # 아기 상어가 자기 크기만큼 물고기를 잡아먹었다면
    if count == size:
        count = 0
        size += 1
```

