출처: 백준 온라인 저지
https://www.acmicpc.net/problem/2529

<br>

___

### 📃 문제 설명

부등호가 주어지면, 그 부등호를 만족시키는 한 자리수들을 배열하여 만들 수 있는 최소 / 최대의 수를 구해야 한다.

예를 들어, 부등호가 `< > >`이라고 하자. 그렇다면 `A < B > C > D`를 만족하는 네 자리수 ABCD를 구해야 한다. 이 경우, 가장 큰 수는 8976이고, 가장 작은 수는 0321이다. (0으로 시작하는 수도 포함한다.)

<br>

### 🔎 풀이 과정

`백트래킹`을 활용하면 된다.

가장 큰 수의 경우, 매 자리마다 9부터 0까지 대입하여, 가장 먼저 완성되는 수를 구하면 된다. 

`< > > <`의 경우를 생각해보자. 일단 맨 앞자리 수에 9를 대입해본다. 그런데 그 다음에는 9보다 큰 수가 와야 하는데, 9보다 큰 한 자리 수는 없으므로, 이러한 경우는 없다. 다시 첫째 자리로 돌아가서 8을 넣는다. 그 뒤로도 계속 9부터 0까지 차례로 살펴보며 넣을 수 있는 가장 큰 수를 넣어본다. 아래와 같은 과정을 거치면 부등호를 만족하는 가장 큰 수가 `89756`임을 알 수 있다.

A < B > C > D < E
`9` < B > C > D < E (불가능)
8 < 9 > C > D < E
8 < 9 > 7 > D < E
8 < 9 > 7 > `6` < E (불가능)
8 < 9 > 7 > 5 < E
8 < 9 > 7 > 5 < 6 (완성!) --> 가장 큰 수는 `89756`

<br>

가장 작은 수는 마찬가지의 방식으로 0부터 9까지 대입하면 구할 수 있다.

그런데 구현 과정에서 한 가지 문제에 봉착했다.

<br>

#### 문제

부등호를 만족하는 가장 큰 수를 구했을 때, 탐색을 종료하는 것을 구현하기 어려웠다는 점이다. 일반적인 DFS의 경우, 이미 방문한 노드에 방문 표시를 하여 탐색을 마치고 나면 더 이상 탐색을 진행하지 않을 수 있다. 하지만 위의 경우에 그렇게 구현할 경우, 89756 다음에도 89746, 89745...과 같이 계속 탐색을 이어가게 된다.

<br>

#### 해결

위 문제를 해결하는 다양한 방법이 있을 것이다.

나의 경우, 함수 외부에 `max_list`라는 빈 리스트를 정의했다. 탐색을 하다가 부등호를 만족시키는 가장 큰 수의 리스트 (위 예제에서는 [8, 9, 7, 5, 6]) 를 발견하면, 해당 리스트를 `max_list`에 저장하도록 했다. 그리고 탐색을 하기 전에, `max_list`가 비어있는지를 확인했다. 만약 `max_list`가 비어있지 않다면, 이미 가장 큰 수를 찾은 것이므로, 더 이상 탐색을 하지 않도록 했다. 이와 같은 방식으로 부등호를 만족하는 가장 큰 수를 찾고 나면, 더 이상 탐색을 이어가지 않도록 했다.

<br>

그렇게 만든 정답 풀이는 아래와 같다.

<br>

### 🔓 첫 정답 풀이

```python

from sys import stdin


# 주어진 부등호 조건을 만족하는 가장 큰 수를 찾아 max_list에 저장하는 함수
def find_max(num_list, i, before):
    global max_list

    # 조건을 만족하는 가장 큰 k자리 수를 찾았다면
    if i >= k:
        max_list = num_list
        return

    for num in range(9, -1, -1):
    	# max_list가 비어있다면 (아직 가장 큰 수를 찾지 못했다면)
        if not max_list:
            # 아직 숫자 num이 사용되지 않았다면
            if num not in num_list:
                # 조건을 만족하는 가장 큰 숫자를 찾으면, 다음 숫자 탐색을 시작한다.
                if input_signs[i] == '<' and before < num:
                    find_max(num_list + [num], i + 1, num)

                if input_signs[i] == '>' and before > num:
                    find_max(num_list + [num], i + 1, num)


# 주어진 부등호 조건을 만족하는 가장 작은 수를 찾아 min_list에 저장하는 함수
def find_min(num_list, i, before):
    global min_list

    # 조건을 만족하는 가장 작은 k자리 수를 찾았다면
    if i >= k:
        min_list = num_list
        return

    for num in range(10):
        # min_list가 비어있다면 (아직 가장 작은 수를 찾지 못했다면)
        if not min_list:
            # 아직 숫자 num이 사용되지 않았다면
            if num not in num_list:
                # 조건을 만족하는 가장 작은 수를 찾으면, 다음 숫자 탐색을 시작한다.
                if input_signs[i] == '<' and before < num:
                    find_min(num_list + [num], i + 1, num)

                if input_signs[i] == '>' and before > num:
                    find_min(num_list + [num], i + 1, num)


k = int(stdin.readline())
input_signs = [x for x in stdin.readline().split()]
max_list = []
min_list = []

for start in range(9, -1, -1):
    if not max_list:
        find_max([start], 0, start)

for start in range(10):
    if not min_list:
        find_min([start], 0, start)

print(str(''.join(map(str, max_list))))
print(str(''.join(map(str, min_list))))
```

<br>

위 코드에서, `find_max` 함수와 `find_min` 함수에는 모두 어떤 수가 등호 조건을 만족하는지를 검사하는 코드가 나온다. 이 부분을 따로 `possible`이라는 함수로 정의하고, 그외 반복되는 부분을 줄여 코드를 보다 깔끔하게 만들었다. 

<br>

### 🔓 최종 풀이

```python

from sys import stdin


# 어떤 수가 부등호 조건을 만족하는지 검사하는 함수
def is_possible(i, before, current):
    if input_signs[i] == '<' and before < current:
        return True
    if input_signs[i] == '>' and before > current:
        return True

    return False


# 주어진 부등호 조건을 만족하는 가장 큰 수를 찾아 max_list에 저장하는 함수
def find_max(num_list, i, before):
    global max_list

    # 조건을 만족하는 가장 큰 k자리 수를 찾았다면
    if i >= k:
        max_list = num_list
        return

    for num in range(9, -1, -1):
        # 아직 가장 큰 수를 찾지 못했고, 숫자 num이 아직 사용되지 않았다면
        if not max_list and num not in num_list:
            if is_possible(i, before, num):
                find_max(num_list + [num], i + 1, num)


# 주어진 부등호 조건을 만족하는 가장 작은 수를 찾아 min_list에 저장하는 함수
def find_min(num_list, i, before):
    global min_list
    
    # 조건을 만족하는 가장 작은 k자리 수를 찾았다면
    if i >= k:
        min_list = num_list
        return

    for num in range(10):
        # 아직 가장 작은 수를 찾지 못했고, 숫자 num이 아직 사용되지 않았다면
        if not min_list and num not in num_list:
            if is_possible(i, before, num):
                find_min(num_list + [num], i + 1, num)


k = int(stdin.readline())
input_signs = [x for x in stdin.readline().split()]
max_list = []
min_list = []

for x in range(10):
    if not max_list:
        find_max([9 - x], 0, 9 - x)
    if not min_list:
        find_min([x], 0, x)

print(str(''.join(map(str, max_list))))
print(str(''.join(map(str, min_list))))
```