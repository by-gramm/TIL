출처: 백준 온라인 저지
https://www.acmicpc.net/problem/14425

<br>

___

### 📃 문제 설명

N개의 문자열 집합 S1과  M개의 문자열 집합 S2가 주어진다.

S1에는 같은 문자열이 없고, S2에는 같은 문자열이 존재할 수 있다.

S1의 문자열 중 S2에 포함된 문자열의 개수를 구해야 한다.


<br>


### ⏰ 처음 풀이

가장 먼저 생각할 수 있는 풀이 방법은, S2의 M개의 문자열을 순회하면서, 각 문자열이 S1에 포함되는지 확인하는 것이다. 이렇게 푼 경우, 시간은 많이 걸리긴 했지만 주어진 조건은 맞출 수 있었다.

```python
from sys import stdin


n, m = map(int, stdin.readline().split())
first_strings = []
count = 0

for _ in range(n):
    new_str = stdin.readline().rstrip()
    first_strings.append(new_str)

for _ in range(m):
    new_str = stdin.readline().rstrip()
    if new_str in first_strings:
        count += 1

print(count)
```


<br>

### 🔓 최종 풀이

하지만 최대 10,000개인 S2의 문자열을 일일이 순회하면서 S1에 포함되는지 확인하는 방법은 비효율적이다. 

S2의 매 문자열마다 S1 전체에서 찾지 않도록, 우선 S1과 S2를 정렬시켰다. 그 이후로는 마치 **투 포인터 알고리즘**과 같이, S1과 S2의 두 값을 비교해나가며 겹치는 값을 찾아나갔다. 

S1의 x번째 값과 S2의 y번째 값을 비교한다고 해보자. 만약 S1의 x번째 값이 더 크다면(문자열상으로 더 뒤라면), S1에서 x번째 값 이후로는 S2의 y번째 값과 같은 값이 결코 나올 수 없다. 그렇다면 더 이상 S2의 y번째 값은 탐색을 할 필요가 없어진다. 그러면 이제 S2의 y + 1번째 값을 다시 S1의 x번째 값과 비교하면 된다.

S1의 문자열 중 S2에 포함된 문자열의 개수는 `count` 변수에 저장한다. 만약 탐색을 하는 도중 비교한 두 값이 같다면, `count`에 1을 더하고, S2의 탐색 인덱스를 1 증가시킨다. 왜 S2의 탐색 인덱스만 증가시킬까? S1의 x번째 값과 S2의 y번째 값이 같다고 하자. S1에는 겹치는 값이 없으므로, S1의 x + 1번째 값은 S2의 y번째 값보다 반드시 크다. 반면 S2는 같은 값이 여러번 나올 수 있으므로,  S2의 y + 1번째 값도 S1의 x번째 값과 같을 수 있다. 따라서 두 값이 같은 경우, S1의 탐색 인덱스는 유지한 채로 S2의 탐색 인덱스만 1 증가시키는 것이다.

위의 내용을 구현한 코드는 아래와 같다. 결과적으로 풀이 시간이 3752ms에서 188ms로 크게 줄었다. 

```python

from sys import stdin


n, m = map(int, stdin.readline().split())
first_strings = []
second_strings = []
count = 0

for _ in range(n):
    new_str = stdin.readline().rstrip()
    first_strings.append(new_str)

first_strings.sort()

for _ in range(m):
    new_str = stdin.readline().rstrip()
    second_strings.append(new_str)

second_strings.sort()

idx1, idx2 = 0, 0

while idx1 < len(first_strings) and idx2 < len(second_strings):
    if first_strings[idx1] == second_strings[idx2]:
        count += 1
        idx2 += 1
    elif first_strings[idx1] > second_strings[idx2]:
        idx2 += 1
    else:
        idx1 += 1
        
print(count)

```

