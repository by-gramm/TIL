출처: 백준 온라인 저지
https://www.acmicpc.net/problem/15903

<br>


### 처음 풀이

```python
from sys import stdin


n, m = map(int, stdin.readline().split())

cards = []
cards += map(int, stdin.readline().split())

for _ in range(m):
    cards.sort()
    cards[0] = cards[1] = cards[0] + cards[1]

print(sum(cards))
```

<br>
풀이 자체는 간단했다. 전체 카드의 합을 가장 작게 하려면, 카드 더미에서 가장 작은 두 수를 골라 두 수의 합을 덮어쓰는 과정을 반복하면 된다. 

그런데 위 풀이보다 2배 이상 시간 효율적인 풀이들이 있었고, 그 풀이들은 `우선순위 큐`를 활용하고 있었다. 우선순위 큐는 heap 자료구조를 통해 구현할 수 있다.

위의 풀이에서는 카드 2개를 고른 뒤, 다시 넣을 때마다 `sort()` 함수로 정렬을 수행하는데, `sort()`의 시간 복잡도는 `O(nlogn)`이다. 

반면 우선순위 큐를 사용하면, 값이 바뀐 카드 2개를 다시 우선순위 큐 자료구조 안에 삽입하기만 하면 된다. heap에서 삽입 연산의 시간 복잡도는 `O(logn)`으로, 훨씬 효율적이다.

파이썬에서는 `heapq` 내장 모듈을 통해 쉽게 힙을 구현할 수 있다. 이때 주의할 점은, heap이 그 자체로 별도의 자료구조는 아니라는 점이다. heap을 생성하는 대신, 빈 리스트를 생성한 뒤 `heapq` 모듈을 통해 리스트를 heap으로 사용할 수 있다.

<br>

#### heap 내용 정리

- heap 생성 : 빈 리스트 생성 (`[]`)

- item을 heap에 삽입 : `heapq.heappush(heap, item)`

- heap의 마지막 요소 삭제 : `heapq.heappop(heap)`

- 리스트 x를 heap으로 변환 : `heapq.heapify(x)`

<br>

### 우선순위 큐를 사용한 풀이

```python
from sys import stdin
import heapq


n, m = map(int, stdin.readline().split())

# heap 생성
cards = []
card_list = [int(x) for x in stdin.readline().split()]

for card in card_list:
    heapq.heappush(cards, card)

for _ in range(m):
    card1 = heapq.heappop(cards)
    card2 = heapq.heappop(cards)

    heapq.heappush(cards, card1 + card2)
    heapq.heappush(cards, card1 + card2)

print(sum(cards))

```

위 풀이에서는 카드의 수들을 리스트로 받은 뒤, 일일이 새로 생성한 heap에 저장하여 카드의 수를 저장하는 heap을 만들었다. 

아래와 같이 리스트를 heap으로 만들어주는 `heapify()` 함수를 활용하면 더욱 간단한 풀이가 가능하다.

<br>

### heapify()를 이용한 풀이

```python
from sys import stdin
import heapq


n, m = map(int, stdin.readline().split())

cards = [int(x) for x in stdin.readline().split()]
# cards 리스트를 heap으로 변환
heapq.heapify(cards)

for _ in range(m):
    card1 = heapq.heappop(cards)
    card2 = heapq.heappop(cards)

    heapq.heappush(cards, card1 + card2)
    heapq.heappush(cards, card1 + card2)

print(sum(cards))
```