출처: 백준 온라인 저지
https://www.acmicpc.net/problem/17136

<br>

___

### ⏰ 시간 초과 풀이

```python

from sys import stdin
from copy import deepcopy


# (r, c)를 왼쪽 위 꼭지점으로 가지는 정사각형의 한 변의 최대 길이를 구하는 함수
def get_max_square(arr, r, c):
    max_value = 1
    # 색종이의 크기는 최대 5 X 5
    for i in range(1, min(10 - r, 10 - c, 5)):
        if arr[r + i][c + i] == 0:
            return max_value
        for j in range(i):
            if arr[r + i][c + j] == 0:
                return max_value
            if arr[r + j][c + i] == 0:
                return max_value
        max_value += 1

    return max_value


# (r, c)를 왼쪽 위 꼭지점으로 가지는 size n의 정사각형을 0으로 바꾸는 함수
def remove_square(arr, r, c, size):
    for i in range(r, r + size):
        for j in range(c, c + size):
            arr[i][j] = 0


"""
arr : 현재 배열
count : 사용된 색종이의 개수
now_r : 현재 탐색 위치의 행
usable_paper : 현재 사용 가능한 색종이 개수를 저장한 배열
"""
# 1이 적인 칸을 모두 붙이는데 필요한 색종이의 최소 개수를 구하는 함수
def get_num_of_square(arr, count, now_r, usable_paper):
    for r in range(now_r, 10):
        for c in range(10):
            if arr[r][c] == 1:
                temp = []
                max_size = get_max_square(arr, r, c)

                for i in range(max_size, 0, -1):
                    # 한 변의 길이가 i인 색종이가 남아 있다면
                    if usable_paper[i]:
                        cp_arr = deepcopy(arr)
                        remove_square(cp_arr, r, c, i)

                        cp_paper = deepcopy(usable_paper)
                        cp_paper[i] -= 1

                        temp.append(get_num_of_square(cp_arr, count + 1, r, cp_paper))
                if temp:
                    return min(temp)
                else:
                    return -1

    return count


boards = []
for _ in range(10):
    boards.append([int(x) for x in stdin.readline().split()])

# 사용 가능한 색종이의 개수
colored = [0, 5, 5, 5, 5, 5]

count_one = 0

for r in range(10):
    for c in range(10):
        if boards[r][c] == 1:
            count_one += 1

# 배열의 모든 값이 1이라면
if count_one == 100:
    print(4)
# 배열의 값 중 0이 있다면
else:
    value = get_num_of_square(boards, 0, 0, colored)
    # 사용 가능한 색종이로 모든 1을 덮을 수 있는 방법이 없다면
    if value == -1:
        print(-1)
    else:
        print(value)
```

<br>

`백트래킹`으로 구현했다.

테스트 케이스 중 배열의 모든 값이 1인 경우 시간이 너무 오래 걸려서, 아예 그 부분은 따로 처리를 해주었다. 

Pypy3으로는 통과했지만, 파이썬 3으로는 시간 초과가 떴다. 


<br>

### 🔑 문제 해결 과정

##### 문제 1

재귀 함수를 통한 백트래킹으로 구현했는데, 함수를 새로 호출할 때마다 현재 배열과 같은 배열을 새로 만들어서 시간 효율성과 공간 효율성이 모두 낮아졌다. 

##### 해결 방안

하나의 색종이를 붙인 상태에서 DFS로 탐색을 마친 뒤에, 그 색종이에 대해서만 원상 복귀를 시킨 다음 다른 색종이를 붙이는 방식으로 구현할 수 있을 것이다. 그래서 붙였던 색종이를 떼어내는 함수를 따로 만들었다. 색종이를 붙이는 함수가 색종이 범위 내의 수를 0으로 바꾼다면, 색종이를 떼어내는 함수는 반대로 이 수들을 1로 바꾸어준다. 

```python

# (r, c)를 왼쪽 위 꼭지점으로 가지는 size n의 색종이를 붙이는 함수
def attach_colored_paper(arr, r, c, size):
    for i in range(r, r + size):
        for j in range(c, c + size):
            arr[i][j] = 0


# (r, c)를 왼쪽 위 꼭지점으로 가지는 size n의 색종이를 떼어내는 함수
def detach_colored_paper(arr, r, c, size):
    for i in range(r, r + size):
        for j in range(c, c + size):
            arr[i][j] = 1
```

<br>

##### 문제 2

남은 색종이의 개수를 저장하는 `colored_paper` 배열도 마찬가지의 문제가 있었다.

##### 해결 방안

역시 매번 새로운 배열을 만드는 대신, DFS로 탐색을 마친 후 원상 복귀를 시켜주면 된다. 사이즈 n의 색종이 하나를 쓰면 `colored_paper[n]`의 값을 1 빼주고, 탐색이 끝나고 나면 그 값에 다시 1을 더해주면 된다.

<br>

### 🔓 최종 풀이

위 문제들을 해결하고 나니 메모리와 시간 모두 크게 단축되어, 파이썬 3으로도 무난하게 통과할 수 있었다. 최종 풀이 코드는 아래와 같다.

```python

from sys import stdin


# (r, c)를 왼쪽 위 꼭지점으로 가지는 정사각형의 한 변의 최대 길이를 구하는 함수
def get_max_square(arr, r, c):
    max_value = 1
    # 색종이의 크기는 최대 5X5
    for i in range(1, min(10 - r, 10 - c, 5)):
        # (r + i, c + i) 확인
        if arr[r + i][c + i] == 0:
            return max_value
        for j in range(i):
            # (r + i, c)부터 (r + i, c + i - 1)까지 확인
            if arr[r + i][c + j] == 0:
                return max_value
            # (r, c + i)부터 (r + i - 1, c + i)까지 확인
            if arr[r + j][c + i] == 0:
                return max_value
        max_value += 1

    return max_value


# (r, c)를 왼쪽 위 꼭지점으로 가지는 size n의 색종이를 붙이는 함수
def attach_colored_paper(arr, r, c, size):
    for i in range(r, r + size):
        for j in range(c, c + size):
            arr[i][j] = 0


# (r, c)를 왼쪽 위 꼭지점으로 가지는 size n의 색종이를 떼어내는 함수
def detach_colored_paper(arr, r, c, size):
    for i in range(r, r + size):
        for j in range(c, c + size):
            arr[i][j] = 1


"""
arr : 현재 배열
count : 사용된 색종이의 개수
now_r : 현재 탐색 위치의 행
papers : 현재 사용 가능한 색종이 개수를 저장한 배열
"""
# 1이 적인 칸을 모두 붙이는데 필요한 색종이의 최소 개수를 구하는 함수
def get_num_of_square(arr, count, now_r, papers):
    # 이전에 탐색하던 열에서부터 탐색을 진행한다.
    for r in range(now_r, 10):
        for c in range(10):
            if arr[r][c] == 1:
                max_size = get_max_square(arr, r, c)
                temp = []

                for i in range(max_size, 0, -1):
                    # 한 변의 길이가 i인 색종이가 남아 있다면
                    if usable_paper[i]:
                        # 백트래킹으로 DFS
                        attach_colored_paper(arr, r, c, i)
                        papers[i] -= 1
                        temp.append(get_num_of_square(arr, count + 1, r, papers))
                        detach_colored_paper(arr, r, c, i)
                        papers[i] += 1

                # (r, c)에 덮을 수 있는 색종이가 하나 이상 존재한다면
                if temp:
                    return min(temp)
                # (r, c)에 덮을 수 있는 색종이가 하나도 없다면 -1 리턴
                else:
                    return -1

    # 배열 내에 더 이상 1이 없는 경우
    return count


boards = []
for _ in range(10):
    boards.append([int(x) for x in stdin.readline().split()])

# 사용 가능한 색종이의 개수
colored = [0, 5, 5, 5, 5, 5]
count_one = 0

for r in range(10):
    for c in range(10):
        if boards[r][c] == 1:
            count_one += 1

# 배열의 모든 값이 1이라면
if count_one == 100:
    print(4)
else:
    value = get_num_of_square(boards, 0, 0, colored)
    # 모든 1을 색종이로 덮을 수 있는 경우가 없다면
    if value == -1:
        print(-1)
    else:
        print(value)
```