## Priority Queue in java

#### 우선순위 큐

- `Stack` 
  - Last In First Out (늦게 들어온 것부터 꺼낸다)

- `Queue` 
  - First In First Out (먼저 들어온 것부터 꺼낸다)

- `Priority Queue` 
  - Highest Priority First Out (우선순위가 높은 것부터 꺼낸다)
  - 주로 heap 자료구조를 통해 구현

<br>

#### 선언

```java
import java.util.PriorityQueue;
import java.util.Collections;


// 기본 선언 형식
PriorityQueue<E> pQueue = new PriorityQueue<E>();

// 선언 예시

// 1. 작은 수일수록 우선순위가 높음
PriorityQueue<Integer> pQueue = new PriorityQueue<>();

// 2. 큰 수일수록 우선순위가 높음
PriorityQueue<Integer> reverseQueue = new PriorityQueue<>(Collections.reverseOrder());

// 3. 알파벳 순으로 앞에 있을수록 우선순위가 높음
PriorityQueue<String> stringQueue = new PriorityQueue<>(); 

// 4. 알파벳 순으로 앞에 있을수록 우선순위가 높음
PriorityQueue<String> reverseStringQueue = new PriorityQueue<>(Collections.reverseOrder());
```

<br>

#### 메서드

- `add(element e)`
  - 우선순위 큐에 원소 e를 넣는다.
- `remove(element e)`
  - 우선순위 큐에서 원소 e를 삭제한다.
- `peek()`
  - 우선순위 큐에서 우선순위가 가장 높은 원소를 반환한다.

- `poll()`
  - 우선순위 큐에서 우선순위가 가장 높은 원소를 반환하며, 동시에 삭제한다.

- `toArray()`
  - 우선순위 큐의 원소들을 배열로 반환한다.

<br>

#### 참고 자료

https://www.geeksforgeeks.org/priority-queue-class-in-java/