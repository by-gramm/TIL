출처: 백준 온라인 저지
https://www.acmicpc.net/problem/3109

<br>

___

### 📃 문제 설명

`R X C` 크기의 지도가 주어진다. 

첫째 열은 근처 빵집의 가스관이고, 마지막 열은 원웅의 빵집이다. 

첫째 열(근처 빵집의 가스관)에서 시작하여, 건물들에 막히지 않고 마지막 열(원웅 빵집의 가스관)로 가스관을 연결해야 한다. 

각 칸은 오른쪽 위, 오른쪽, 오른쪽 아래 중 하나로 연결할 수 있다. 

이때 두 가스관을 연결하는 파이프라인의 최대 개수를 구해야 한다.

<br>

### ⏰ 시간 초과 풀이

그리디와 백트래킹을 결합한 방식으로 구현해보았다.

`그리디`

첫째 열의 첫 행에서부터 가능한 파이프라인의 경로를 탐색한다. 파이프라인을 겹치지 않고 최대한 많이 만들기 위해서는, 매 순간 최대한 위쪽으로 붙는 경로를 탐색해야 한다. 그래서 매 지점마다 오른쪽 위 대각선, 오른쪽, 오른쪽 아래 대각선 순으로 탐색을 이어나간다. 

`백트래킹`

탐색을 하던 도중 오른쪽 위/오른쪽/오른쪽 아래 중 어디로도 파이프라인을 연결할 수 없다면, 탐색을 중단하고 이전 위치로 돌아간다. 첫째 열부터 마지막 열까지 이어진 경로를 찾아내면, 해당 탐색을 종료하고, 파이프라인의 수를 저장하는 변수 count에 1을 더한다.

<br>

첫째 열의 첫 행부터 마지막 행까지 위와 같은 방식으로 탐색을 진행하고 나면, count 변수에 최대 파이프라인의 수가 저장될 것이다. 

아래는 위의 방식을 구현한 코드다. 시간 초과가 떴다.

```python

from sys import stdin


def search_route(arr, row, col):
    # 마지막 행에 도착했다면 탐색 종료
    if col == c:
        return 1

    # 오른쪽 위 대각선 경로 탐색
    if arr[row - 1][col + 1] == '.':
        # 방문 표시
        arr[row - 1][col + 1] = 'x'
        # 경로가 존재한다면 탐색 종료
        if search_route(arr, row - 1, col + 1):
            return 1
        # 경로가 존재하지 않는다면 이전 위치로 복귀
        else:
            arr[row - 1][col + 1] = '.'

    # 오른쪽 경로 탐색
    if arr[row][col + 1] == '.':
        arr[row][col + 1] = 'x'
        if search_route(arr, row, col + 1):
            return 1
        else:
            arr[row][col + 1] = '.'

    # 오른쪽 아래 대각선 경로 탐색
    if arr[row + 1][col + 1] == '.':
        arr[row + 1][col + 1] = 'x'
        if search_route(arr, row + 1, col + 1):
            return 1
        else:
            arr[row + 1][col + 1] = '.'

    # 오른쪽 위/오른쪽/오른쪽 아래 중 어디에도 경로가 없다면 0을 반환
    return 0


r, c = map(int, stdin.readline().split())
boards = [['x'] * (c + 1)]
for _ in range(r):
    boards.append(['x'] + list(stdin.readline().rstrip()))
boards.append(['x'] * (c + 1))

count = 0

for i in range(1, r + 1):
    count += search_route(boards, i, 1)

print(count)
```

<br>

### 🔎 문제 해결 과정

위 풀이가 비효율적인 이유는, 같은 경로를 여러번 반복하여 탐색하기 때문이다. 

`(1, 1)`에서 오른쪽 아래 대각선으로 가는 경로를 탐색했는데, 마지막 행까지 갈 수 있는 경로가 없었다고 해보자. 그렇다면 `(2, 2)`를 지나는 경로는 존재하지 않는다. 

그런데 이후에 `(3, 1)`에서 오른쪽 위 대각선으로 가는 경로를 탐색한다고 하자. `(2, 2)`를 지나는 경로는 존재하지 않으므로, 애초에 `(3, 1)`에서 오른쪽 위 대각선으로 가는 경로는 탐색할 필요가 없다. 그런데 `(2, 2)`로 시작하는 경로가 없다는 것을 따로 표시하지 않았으므로, 아까 했던 탐색을 다시 반복하게 된다.

따라서 `(r, c)`를 지나는 경로가 없다는 것을 알게 되면, 이를 표시해 주어야 한다. 표시하는 방법은 간단하다. 'x'로 방문 표시를 했던 해당 위치를 '.'로 다시 바꾸지 않는 것이다. 그렇다면 이후에 같은 위치를 다시 탐색하지 않게 된다.

이와 같이 구현했더니 이번에는 시간 초과가 뜨지 않았다.

<br>

### 🔑 정답 풀이

```python

from sys import stdin


def search_route(arr, row, col):
    # 마지막 행에 도착했다면 탐색 종료
    if col == c:
        return 1

    # 오른쪽 위 대각선 경로 탐색
    if arr[row - 1][col + 1] == '.':
        # 방문 표시
        arr[row - 1][col + 1] = 'x'
        # 경로가 존재한다면 탐색 종료
        if search_route(arr, row - 1, col + 1):
            return 1

    # 오른쪽 경로 탐색
    if arr[row][col + 1] == '.':
        arr[row][col + 1] = 'x'
        if search_route(arr, row, col + 1):
            return 1

    # 오른쪽 아래 대각선 경로 탐색
    if arr[row + 1][col + 1] == '.':
        arr[row + 1][col + 1] = 'x'
        if search_route(arr, row + 1, col + 1):
            return 1

    # 오른쪽 위/오른쪽/오른쪽 아래 중 어디에도 경로가 없다면 0을 반환
    return 0


r, c = map(int, stdin.readline().split())
boards = [['x'] * (c + 1)]
for _ in range(r):
    boards.append(['x'] + list(stdin.readline().rstrip()))
boards.append(['x'] * (c + 1))

count = 0

for i in range(1, r + 1):
    count += search_route(boards, i, 1)

print(count)
```