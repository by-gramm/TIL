## Semaphore

> Semaphore는 주차장이다.
>
> 특정 자원이나 자원 그룹에 접근하는 사용자 수를 제한하는 데 사용된다.

#### 사용 방법

- `acquire()`
  - 스레드가 semaphore의 permit을 하나 가져간다.
- `acquire(int permits)`
  - permits 개수 만큼의 permit을 가져간다.
- `release()`
  - 스레드가 permit 하나를 놓아준다.
- `release(int permits)`
  - permits 개수 만큼의 permit을 놓아준다.
- **주의) acquire하지 않은 스레드가 release할 수 있다.**

#### Lock과의 비교

1. Lock은 자원당 한 명의 유저만 접근 가능하지만, Semaphore는 여러 유저가 동시에 접근 가능하다.

   - Semaphore는 **소유자 스레드**의 개념이 없다.

   - 하나의 스레드가 semaphore를 여러 번 얻을 수 있다.

2. semaphore를 얻지 않은 스레드도 semaphore를 release할 수 있다.

#### 활용 - Producer Consumer

```java
Semaphore full = new Semaphore(0);
Semaphore empty = new Semaphore(CAPACITY);
Queue queue = new ArrayDeque();
Lock lock = new ReentrantLock();

// Producer
while (true) {
    Item item = produce();     // 2. 새로운 Item을 생산한다.
    empty.acquire();           // 3. empty 세마포어의 permit을 얻는다. 단, empty 세마포어에서 남은 permit이 없는 경우 block된다.
    lock.lock();
    queue.offer(item);         // 4. Lock을 획득해서 Item을 Queue에 넣는다.
    lock.unlock();
    full.release();            // 5. full 세마포어를 release한다.
}

// Consumer
while (true) {
    full.acquire();            // 1. full 세마포어에 의해 block된다.
    lock.lock();
    Item item = queue.poll();  // 6. block이 해제된 뒤, Lock을 획득해서 Queue의 Item을 가져온다.
    lock.unlock();
    consume(item);             // 7. Item을 consume한다.
    empty.release();           // 8. empty 세마포어의 permit을 release한다. 만약 block되어 있던 Producer가 있다면, 해당 Producer는 block이 해제된다.
}
```

<br>

## Inter-thread Communication

- 앞서 살펴본 스레드 간 통신의 예시
  - `Thread.interrupt()`
    - 스레드가 일시정지 상태에 있는 경우 InterruptedException을 발생시킨다.
  - `Thread.join()`
    - 다른 스레드가 종료할 때까지 기다린다.
  - `Semaphore.release()`
    - block된 다른 스레드를 깨워서 세마포어의 permit을 얻을 수 있도록 한다.

#### 조건 변수 (Condition Variables)

- semaphore는 조건 변수의 특별한 사례다.
  - semaphore의 acquire() 메소드 호출은 "permit의 개수 > 0"이라는 조건을 확인하는 것과 같다.
  - 조건이 만족하지 않으면, 스레드는 다른 스레드가 세마포어의 상태를 변화시킬 때까지 잠들어 있는다.
  - 다른 스레드가 release() 메소드를 호출하면, 잠들어 있던 스레드가 깨어나고, "permit의 개수 > 0" 조건이 만족하는지 확인한다.
- 조건 변수의 동작 방식
  - 스레드 A가 조건을 검사한다. 조건이 충족되지 않으면 스레드 A는 block된다.
  - 이후 스레드 B가 세마포어의 상태를 변경한 뒤, 스레드 A에 신호를 보내 깨운다.
  - 깨어난 스레드 A는 다시 조건을 검사한다. 조건이 충족되면 작업을 지속하고, 충족되지 않으면 다시 block된 채로 기다린다.
- 조건 변수 생성

```java
Lock lock = new ReentrantLock();
Condition condition = lock.newCondition();
```

- `void Condition.await()`
  - 다른 스레드가 신호를 보내 깨울 때까지 스레드를 잠들게 한다.
- `void Condition.signal()`
  - 현재 조건 변수에서 기다리는 스레드 중 하나를 깨운다.
  - 조건 변수에 기다리는 스레드가 없다면, 아무런 일도 일어나지 않는다.
    - 이후에 호출되는 await() 메소드에는 영향을 주지 않는다.
- `void Condition.signalAll()`
  - 현재 조건 변수에서 기다리는 모든 스레드를 깨운다.
  - semaphore와의 비교
    - semaphore에서는 현재 기다리는 스레드의 수만큼 release()를 호출해야 한다.
    - 반면 조건 변수는 현재 기다리는 스레드의 수를 몰라도 signalAll()로 모든 스레드를 깨울 수 있다.

#### wait(), notify(), notifyAll()

- Java의 Object 클래스는 wait() | notify() |notifyAll() 메소드를 포함한다.
  - 이 메소드들을 통해 어떠한 객체도 조건 변수로 사용 가능하다.
- `public final void wait() throws InterruptedException`
  - 다른 스레드가 깨어날 때까지 현재 스레드를 기다리게 한다.
- `public final void notify()`
  - 현재 객체에서 대기하는 스레드 중 하나를 임의로 깨운다.
- `public final void notifyAll()`
  - 현재 객체에서 대기하는 모든 스레드를 깨운다.
- 단, wait() | notify() | notifyAll() 메소드를 호출하려면, 우선 객체를 동기화해야 한다.

