# [Python] 프로그래머스 - 표 편집

출처: 프로그래머스 코딩 테스트 연습

https://programmers.co.kr/learn/courses/30/lessons/81303



### 문제 접근

주어진 표에 대하여, 아래의 4가지 명령어의 목록이 주어진다.

1. `U X` : X칸 앞의 행 선택하기
2. `D X` : X칸 뒤의 행 선택하기
3. `X` : 현재 행 삭제 후, 바로 아래 행 선택하기 (단, 마지막 행을 삭제한 경우 바로 윗 행 선택)
4. `Z` : 가장 최근에 삭제한 행 복구하기

표의 행의 개수는 최대 1,000,000개이며, 명령어는 최대 200,000개가 주어진다.

<br>

순서가 있는 데이터를 저장하는 자료구조는 크게 Array와 Linked List가 있다. 

**Array**

- 탐색의 시간 복잡도 : `O(1)`
- 삽입/삭제의 시간 복잡도 : `O(N)`

**Linked List**

- 탐색의 시간 복잡도 : `O(N)`
- 삽입/삭제의 시간 복잡도 : `O(1)`

위 문제에서는 삽입/삭제가 자주 일어난다. 따라서 매 삽입/삭제 시마다 `O(N)`이 소요되는 Array보다는 Linked List를 사용하는 것이 시간 효율적이다. 

또한 위 문제에서는 인덱스로 값을 찾는 것이 아니라, 현재 행에서 X칸 앞/뒤의 데이터를 탐색한다. 따라서 Linked List에서도 `O(X)`의 시간 복잡도로 값을 검색할 수 있다. 문제의 조건상 X의 총합이 100만 이하이므로, 탐색에서의 시간 복잡도 문제도 발생하지 않는다.

<br>

### 첫 풀이 (오답)

```python
from collections import deque


class Node:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None


def solution(n, k, cmd):
    # 삭제 요소 목록 (먼저 삭제된 순으로)
    deleted = deque()
    
    # 1. n개의 Node로 이루어진 연결 리스트를 만든다.
    before = Node(0)
    
    if k == 0:
        current = before
    
    for i in range(1, n):
        node = Node(i)
        
        if i == k:
            current = node
            
        before.next = node
        node.prev = before
        before = node
        
    # 2. 각 명령어를 실행한다.
    for x in cmd:
        if x == 'Z':
            # 가장 최근에 삭제된 노드 정보를 복구한다.
            num, left, right = deleted.pop()
            node = Node(num)
            
            # 복구한 노드를 좌우 노드와 연결한다.
            if left is not None:
                left.next = node
                node.prev = left
            if right is not None:
                node.next = right
                right.prev = node
        elif x == 'C':
            # deleted에 현재 노드 값과 좌우 연결 노드 정보를 저장
            deleted.append([current.value, current.prev, current.next])
            
            # 현재 노드가 head node인 경우
            if current.prev is None:
                current.next.prev = None
                current = current.next
            # 현재 노드가 tail node인 경우
            elif current.next is None:
                current.prev.next = None
                current = current.prev
            # 현재 노드가 head node나 tail node가 아닌 경우
            else:
                current.prev.next = current.next
                current.next.prev = current.prev
                current = current.next
        else:
            command, num = x.split()
            
            if command == 'U':
                for _ in range(int(num)):
                    current = current.prev
            else:
                for _ in range(int(num)):
                    current = current.next
    
    result_arr = ["X"] * n
    result_arr[current.value] = "O"
    left, right = current, current

    while left.prev != -1:
        left = left.prev
        result_arr[left.value] = "O"

    while right.!= -1:
        right = right.next
        result_arr[right.value] = "O"
    
    return "".join(result_arr)
```

- 결과 : 테스트케이스 40개 중 15개 통과

- 위 코드의 문제 : 노드를 삭제할 때, 좌우 노드 정보를 함께 저장하고, 복구할 때 새로운 노드를 만들어 기존 연결 리스트에 연결한다. 노드 10개가 있을 때 아래의 단계를 수행한다고 하자.
  - 3번째 노드 삭제
  - 2번째 노드 삭제
  - 2번째 노드 복구
  - 3번째 노드 복구
- 위 단계에서 2번째 노드를 복구할 때, 기존 노드를 다시 사용하지 않고 같은 값을 가진 새로운 노드를 만든다. 이때 새로 만들어진 노드는 기존의 2번째 노드와 주소가 다르다. 3번째 노드를 삭제할 때 함께 저장한 prev 노드와 주소가 다른 것이다. 따라서 이후 3번째 노드를 복구할 때, prev 노드에는 새로 만든 2번째 노드가 아니라, 이미 연결이 끊어진 과거의 2번째 노드가 저장된다. 이런 식으로 연결 리스트가 제대로 저장되지 않는 것이다.

<br>

### 정답 풀이 1

위 문제를 해결한 풀이는 아래와 같다.

```python
from collections import deque


class Node:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None


def solution(n, k, cmd):
    # 삭제 요소 목록
    deleted = deque()
    
    # 1. n개의 Node로 이루어진 연결 리스트를 만든다.
    node_list = [Node(i) for i in range(n)]
    
    for i in range(1, n):
        node_list[i].prev = node_list[i - 1]
        node_list[i - 1].next = node_list[i]
    
    current = node_list[k]
        
    # 2. 각 명령어를 실행한다.
    for x in cmd:
        if x == 'Z':
            num = deleted.pop()
            node = node_list[num]
            
            if node.prev:
                node.prev.next = node
            if node.next:
                node.next.prev = node
        elif x == 'C':
            deleted.append(current.value)
            
            # 현재 노드가 head node인 경우
            if current.prev is None:
                current.next.prev = None
                current = current.next
            # 현재 노드가 tail node인 경우
            elif current.next is None:
                current.prev.next = None
                current = current.prev
            # 현재 노드가 head node나 tail node가 아닌 경우
            else:
                current.prev.next = current.next
                current.next.prev = current.prev
                current = current.next
        else:
            command, num = x.split()
            
            if command == 'U':
                for _ in range(int(num)):
                    current = current.prev
            else:
                for _ in range(int(num)):
                    current = current.next
    
    result = ["O"] * n
    
    while deleted:
        result[deleted.pop()] = "X"
    
    return "".join(result)
```

노드들을 node_list에 저장한 뒤, 삭제할 때는 연결을 끊었다가 복구할 때 기존 노드를 다시 연결하도록 구현했다. 

<br>

### 정답 풀이 2

Node 클래스를 만들지 않고, 좌우 연결 노드의 인덱스를 저장하는 배열을 추가로 만드는 방식으로도 풀어보았다.

```python
from collections import deque


def solution(n, k, cmd):
    # left[i]: i번째 노드의 이전 노드의 인덱스
    left = [i - 1 for i in range(n)]
    left[0] = None
    
    # right[i]: i번째 노드의 다음 노드의 인덱스
    right = [i + 1 for i in range(n)]
    right[n - 1] = None
    
    deleted = deque()
    current = k
        
    for x in cmd:
        if x == 'Z':
            num = deleted.pop()
            
            if left[num]:
                right[left[num]] = num
            if right[num]:
                left[right[num]] = num
        elif x == 'C':
            deleted.append(current)
            
            # 현재 노드가 head node인 경우
            if left[current] is None:
                left[right[current]] = None
                current = right[current]
            # 현재 노드가 tail node인 경우
            elif right[current] is None:
                right[left[current]] = None
                current = left[current]
            # 현재 노드가 head node나 tail node가 아닌 경우
            else:
                right[left[current]] = right[current]
                left[right[current]] = left[current]
                current = right[current]
        else:
            command, num = x.split()
        
            if command == 'U':
                for _ in range(int(num)):
                    current = left[current]
            else:
                for _ in range(int(num)):
                    current = right[current]
    
    result = ["O"] * n
    
    while deleted:
        result[deleted.pop()] = "X"
    
    return "".join(result)
```

길이가 최대 100만인 리스트가 3개(node_list, left, right) 만들어지기 때문에 공간 효율성은 떨어질 수 있지만, 이전/이후 노드를 인덱스만으로 접근하기 때문에 시간적으로는 첫번째 정답 풀이보다 더욱 효율적이다.