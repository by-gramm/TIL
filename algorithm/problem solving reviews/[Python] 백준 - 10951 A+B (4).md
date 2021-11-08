출처: 백준 온라인 저지
https://www.acmicpc.net/problem/10951

<br>

___

### 🔑 풀이 과정

<br>

BFS/DFS 풀고 머리 식힐겸 쉬운 구현 문제에 도전했는데 못 풀었다... 오래 붙잡고 있었다면 풀 수도 있었겠지만 구현 문제라 바로 다른 사람들의 풀이를 참고했다.

이 문제의 핵심은 테스트 케이스의 개수를 알 수 없을 때, 입력이 없음을 판단하여 프로그램을 종료시켜야 한다는 점이다. 크게 2가지 방법으로 이를 구현할 수 있다.

<br>

##### i) try ~ except문을 활용하는 방법

반복문 내에서 try ~ except문을 사용한다. try문에서 매 줄마다 숫자 2개를 변수에 입력받은 뒤, 연산의 값을 반환한다. 그런데 만약 더 이상 입력값이 없다면, 변수에 숫자를 입력할 때 오류가 발생할 것이다. 그 경우, 테스트 케이스가 끝났으므로 except문을 통해 반복문을 나가면 된다.

<br>

##### ii) sys.stdin을 활용하는 방법

sys.stdin을 통해 여러 줄을 한꺼번에 입력받을 수 있다. 그 다음, 이를 for문으로 순회하면, 매 줄마다 순회할 수 있다. 테스트 케이스가 끝나면 물론 for문도 끝날 것이다.


<br>

### 🔓 최종 풀이 1

```python
from sys import stdin


while True:
    try:
        a, b = map(int, stdin.readline().split())
        print(a + b)
    except:
        break
```

<br>

### 🔓 최종 풀이 2

```python
from sys import stdin


for line in stdin:
    a, b = map(int, line.split())
    print(a + b)
```