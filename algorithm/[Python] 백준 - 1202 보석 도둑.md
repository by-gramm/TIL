출처: 백준 온라인 저지
https://www.acmicpc.net/problem/1202

<br>

___

### ⏰ 시간 초과 풀이

```python

from sys import stdin
from bisect import bisect_left


n, k = map(int, stdin.readline().split())

jewels = []
for _ in range(n):
    jewels.append([int(x) for x in stdin.readline().split()])

# 무게를 기준으로 오름차순 정렬
jewels.sort(key=lambda x: x[0])
# 가격을 기준으로 내림차순 정렬
jewels.sort(key=lambda x: x[1], reverse=True)

weights = []
for _ in range(k):
    weights.append(int(stdin.readline()))

weights.sort()


visited = [False] * (k + 1)

total, i = 0, 0

for jw in jewels:
    current = bisect_left(weights, jw[0])
    while visited[current]:
        current += 1
    if current < k:
        total += jw[1]
        visited[current] = True

print(total)
```

<br>

- 보석의 (무게, 가격) 쌍(`jewels`)은

  1) 가격이 높은 것이 먼저 오고
  2) 가격이 같을 경우 가벼운 것이 먼저 오도록 정렬하였다.

- 가방이 담을 수 있는 무게(`weights`)는 오름차순으로 정렬하였다.

<br>

정렬된 (무게, 가격) 쌍으로 이루어진 `jewels` 리스트를 for문으로 순회하면서,

이진 탐색으로 해당 보석을 담을 수 있는 가방 중 `weights` 리스트의 가장 앞에 있는 가방, 즉 담을 수 있는 무게가 가장 적은 가방을 골랐다.

이렇게 매번

1. 남은 보석 중 가장 비싼 보석을
2. 가장 적은 무게를 담을 수 있는 가방에 담는 

`그리디`한 방식으로 구현하였다. 알고리즘 자체는 틀리지 않았지만 시간 초과가 떴다.

<br>

### 🔑 문제 분석

결국 시간 초과를 해결하지 못하여 다른 풀이들을 참고했다.

[참고 풀이 1](https://kyoung-jnn.tistory.com/entry/%EB%B0%B1%EC%A4%801202%EB%B2%88%ED%8C%8C%EC%9D%B4%EC%8D%ACPython-%EB%B3%B4%EC%84%9D-%EB%8F%84%EB%91%91-%EC%9A%B0%EC%84%A0%EC%88%9C%EC%9C%84-%ED%81%90)  | [참고 풀이 2](https://velog.io/@piopiop/%EB%B0%B1%EC%A4%80-1202-%EB%B3%B4%EC%84%9D-%EB%8F%84%EB%91%91-Python)

<br>

우선순위 큐로 **최대 힙**과 **최소 힙**을 구현하여 풀 수 있다.

1. `jewels` 리스트는 우선순위 큐에 저장하고, `weights` 리스트는 앞에서와 마찬가지로 무게 순으로 정렬한다.

2. 보석이 아니라 매 가방을 기준으로 가방에 담을 수 있는 보석을 탐색한다. **최소 힙**을 통해 매번 가방에 담을 수 있는 모든 보석을 찾고, 그것들의 가격을 새로운 우선순위 큐(`jewel_prices`)에 저장한다.

	하나의 가방에 담을 수 있는 보석을 찾은 다음, 다음 가방에 담을 수 있는 보석을 찾을 때는, 이전에 탐색이 끝난 지점에서 이어갈 수 있다. 현재 탐색하는 가방은 이전에 탐색한 가방보다 용량이 더 크거나 같으므로, 앞선 가방에 담을 수 있는 보석은 현재 가방에도 담을 수 있기 때문이다.
   
3. 매번 가방에 담을 수 있는 모든 보석을 찾은 후에는, 그중 가격이 가장 높은 보석을 가방에 담는다. 가방에 담을 수 있는 보석의 가격을 우선순위 큐에 저장했으므로, **최대 힙**을 통해 그중 가장 높은 가격 하나를 꺼내면 된다.

<br>

위의 풀이를 구현한 코드는 아래와 같다.

<br>

### 🔓 정답 풀이

```python

from sys import stdin
import heapq


n, k = map(int, stdin.readline().split())

jewels = []
# (무게, 가격) 쌍의 jewels 리스트를 우선순위 큐에 저장
for _ in range(n):
    heapq.heappush(jewels, [int(x) for x in stdin.readline().split()])

weights = []
for _ in range(k):
    weights.append(int(stdin.readline()))

# 가방을 무게순으로 오름차순 정렬
weights.sort()

total = 0
jewel_prices = []

for bag in weights:
    # jewels 리스트를 우선순위 큐에 저장했으므로,
    # jewels[0]에는 가장 가벼운 보석의 정보가 들어 있음.
    
    # 현재 탐색 중인 가방이 남은 보석 중 가장 가벼운 보석보다 무겁거나 같다면
    while jewels and bag >= jewels[0][0]:
        # 최소 힙을 통해 가장 가벼운 보석을 꺼내고, 그 보석의 가격을 current에 저장함.
        current = heapq.heappop(jewels)[1]
        # 파이썬에는 최소 힙만 존재하므로, 최대 힙은 - 부호를 통해 구현
        heapq.heappush(jewel_prices, -current)
    if jewel_prices:
        # 최대 힙을 통해 가방에 넣을 수 있는 보석의 최대 가격을 total에 더함.
        total -= heapq.heappop(jewel_prices)

print(total)

```