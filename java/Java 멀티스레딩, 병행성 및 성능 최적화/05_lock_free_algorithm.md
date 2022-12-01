## Lock의 단점

1. deadlock
   - Lock이 많을수록 deadlock의 발생 가능성은 커진다.

2. slow critical section
   - 같은 Lock을 사용하는 여러 스레드가 있는 경우, 스레드 하나가 Lock을 너무 오래 가지고 있으면, 다른 모든 스레드는 그만큼 느려진다.

3. priority inversion
   - 우선순위가 낮은 스레드가 Lock을 가진 상태로 선점되는 경우, 우선순위가 높은 스레드가 Lock을 취득하고자 할 때 취득하지 못하게 된다.
4. thread not releasing a lock
   - Lock을 지닌 스레드가 죽거나, 인터럽트되거나, Lock 반환을 잊어버린 경우, 다른 모든 스레드는 정체된다. 
5. performance
   - Lock을 취득하는 과정에서 오버헤드가 발생한다.

<br>

## Lock-Free 알고리즘 

- 연산을 활용하여 단일 하드웨어 명령어로 실행될 수 있도록 보증한다.
- **단일 하드웨어 명령어**
  - 의미상으로 atomic해서 thread-safe한 명령어
- How?
  - AtomicInteger, AtomicLong, AtomicReference 등을 활용한다.
- 주의) Lock-Free 알고리즘이 Lock을 활용하는 방식보다 반드시 더 나은 성능을 보장하지는 않는다.

#### AtomicInteger

- 정수 값으로 실행할 수 있는 원자적 연산을 제공하는 클래스
- 생성
  - 원자적 정수의 객체를 생성하고 정수의 초기값을 생성자에 입력한다.

```java
int initialValue = 0;
AtomicInteger atomicInteger = new AtomicInteger(initialValue);
```

- 주요 메소드

  - `incrementAndGet()`
    - 정수를 atomic하게 1 증가시키고 증가시킨 **새로운** 값을 리턴한다.
  - `getAndIncrement()`
    - 정수를 atomic하게 1 증가시키고 증가시키기 **이전의** 값을 리턴한다.

  - `decrementAndGet()`
    - 정수를 atomic하게 1 감소시키고 감소시킨 **새로운** 값을 리턴한다.
  - `getAndDecrement()`
    - 정수를 atomic하게 1 감소시키고 감소시키기 **이전의** 값을 리턴한다.
  - `addAndGet(int val)`
    - 인자 값만큼 정수를 증가시키고 **새로운** 값을 리턴한다. (음수 가능)

  - `getAndAdd(int val)`
    - 인자 값만큼 정수를 증가시키고 **이전의** 값을 리턴한다. (음수 가능)

- 장점
  - Lock이나 동기화가 필요하지 않아, race condition이나 data race를 신경쓰지 않아도 된다.
- 단점
  - 원자적 연산끼리는 여전히 race condition이 존재할 수 있다.

- 유사하게 AtomicLong, AtomicBoolean 등도 사용 가능하다.

#### AtomicReference

- 클래스의 객체에 대한 레퍼런스를 감싸서, 해당 레퍼런스에서 원자적 연산을 수행할 수 있도록 한다.
- 주요 메소드
  - `AtomicReference(V initialValue)`
  - `V get()`
    - 현재 값을 리턴한다.
  - `void set(V newValue)`
    - newValue로 값을 변경한다.
  - `boolean compareAndSet(V expectedValue, V newValue)` **(중요!)**
    - 현재값이 expectedValue과 일치하면 newValue를 할당하고, 일치하지 않으면 무시한다.
    - 모든 원자적 클래스에서 사용 가능하다.
    - 여러 원자적 연산이 내부적으로 compareAndSet으로 구현된다.

#### 예시 : Lock-Free Stack

```java
public static class LockFreeStack<T> {
    private AtomicReference<StackNode<T>> head = new AtomicReference<>();
    private AtomicInteger counter = new AtomicInteger(0);

    public void push(T value) {
        StackNode<T> newHeadNode = new StackNode<>(value);

        while (true) {
            StackNode<T> currentHeadNode = head.get();
            newHeadNode.next = currentHeadNode;
            if (head.compareAndSet(currentHeadNode, newHeadNode)) {
                break;
            } else {
                LockSupport.parkNanos(1);
            }
        }
        counter.incrementAndGet();
    }

    public T pop() {
        StackNode<T> currentHeadNode = head.get();
        StackNode<T> newHeadNode;

        while (currentHeadNode != null) {
            newHeadNode = currentHeadNode.next;
            if (head.compareAndSet(currentHeadNode, newHeadNode)) {
                break;
            } else {
                LockSupport.parkNanos(1);
                currentHeadNode = head.get();
            }
        }
        counter.decrementAndGet();
        return currentHeadNode != null ? currentHeadNode.value : null;
    }

    public int getCounter() {
        return counter.get();
    }
}
```

- 여러 스레드가 동시에 push()나 pop()을 호출하는 경우, thread-safe하지 않을 수 있다.
- thread-safe함을 보장하기 위해, 위 코드에서는 push()나 pop()에서 필요한 연산을 수행한 뒤 compareAndSet() 메소드로 자신이 바라보고 있던 헤드 노드가 유지되고 있음을 확인한다.
  - 만약 push()나 pop()을 하는 사이에 헤드 노드가 변경되었다면 compareAndSet()은 false를 리턴할 것이고, 그러한 경우 성공할 때까지 다시 연산을 수행하게 된다.

