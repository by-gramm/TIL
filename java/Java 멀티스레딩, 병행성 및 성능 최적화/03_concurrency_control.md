## synchronization

#### atomic operation (원자적 연산)

- **critical section (임계 영역)**

  - 공유 자원에 접근하는 코드로, **원자적으로 실행되어야 하는 코드**

- ex. `count++` => atomic operation이 아니다!

  1. count의 현재 값을 가져온다.

  2. 가져온 값에 1을 더한다.

  3. 증가시킨 값을 count 변수에 다시 저장한다.

- 어떤 연산이 atomic한가?
  - 모든 참조형 할당은 atomic하다.
  - long과 double을 제외한 모든 원시형 할당은 atomic하다.
    - long과 double은 2개의 32bit 값으로 간주되기 때문에 atomic하지 않을 수 있다.
    - 해결 방법 : `volatile` 키워드 사용
      - long이나 double 변수에 volatile 키워드를 사용하면, 해당 변수에 읽고 쓰는 작업이 thread-safe한 원자적 연산이 된다.

```java
public class CounterClass {
    private volatile long counter;

    public void increment() {
        counter++;
    }

    public long getCounter() {
        return counter;
    }
}
```

- 위 코드에서 counter 변수에 volatile 키워드를 사용했기 때문에, getCounter()는 atomic하다.

- 하지만 increment()는 여러 연산이 필요하기 때문에 atomic하지 않다.

#### synchronized 키워드를 활용한 동기화

- 여러 스레드가 critical section이나 메소드 전체에 동시에 접근하는 것을 제한한다.
- 방법 1 : **Monitor**
  - 메소드에 synchronized 키워드를 사용하여, 메소드 전체를 동기화한다.
  - 아래 코드에서 스레드 A가 increment()를 실행하면
    - 스레드 B는 increment()와 decrement()를 모두 실행할 수 없다.

```java
public class Counter {
    private int count = 0;
    
    public synchronized void increment() {
        count++;
    }
    
    public synchronized void decrement() {
        count--;
    }
}
```

- 방법 2 : **Lock**
  - critical section 블록을 정의하고, synchronized 키워드를 사용하여, 해당 영역만 동기화한다.
  - 아래 코드에서 스레드 A가 임계 영역을 실행 중이라면
    - 스레드 B는 스레드 A가 임계 영역을 빠져나올 때까지 임계 영역에 접근할 수 없다.
  - 메소드 전체를 동기화하는 방식에 비해 동시성이 높아져 성능상의 이점이 있다.

```java
public class Counter {
    private int count = 0;
    
    Object lock = new Object();
    
    public void increment() {
        synchronized(this.lock) {
            count++;
        }
    }
    
    public void decrement() {
        synchronized(this.lock) {
            count--;
        }
    }
}
```

<br>

## Race Condition & Data Race

#### Race Condition (경쟁 상태)

- 공유 자원에 접근하는 여러 스레드가 있고, 하나 이상의 스레드가 자원을 수정할 때, 스레드 스케줄링의 순서나 타이밍에 따라 결과가 달라지는 상황
- 문제의 핵심 : 공유 자원에 비원자적 연산이 실행되는 것
- 해결 방법 : `synchronized` 키워드 사용

#### Data Race (데이터 경쟁)

- 컴파일러와 CPU가 성능 최적화와 하드웨어 활용을 위해 비순차적으로 명령을 처리하는 경우가 있다.
  - 이를 통해 프로그램 처리 속도를 높인다.

- 다만, 비순차적인 처리는 논리를 위반하지 않는 경우에 한해서 적용된다.

```java
// 연산 순서와 관계 없이 결과가 동일하므로 연산이 비순차적으로 실행될 수 있다.
public void increment() {
    x++;
    y++;
}

// 코드가 이전 코드의 결과에 의존하므로 비순차적으로 실행될 수 없다.
public void calculate() {
    x = 3;
    y = 3;
    x += y;
    y *= x;
}
```

- 문제는 명령이 비순차적으로 처리될 때, 멀티스레드 환경에서 여러 스레드가 같은 자원에 접근하면 처리 순서에 따라 결과가 달라질 수 있다는 점이다.
- Data Race 해결책
  1. synchronized 키워드를 사용해서 메소드 동기화하기
  2. 공유 변수에 volatile 키워드를 사용해서 처리 순서 보장하기

<br>

## Locking

#### Fine-Grained Locking vs Corase-Grained Locking

- **corase-grained locking**
  - 모든 공유 자원을 하나의 Locking으로 제한한다.
- **fine-grained locking**
  - 각 자원마다 개별 Locking을 건다.
  - 장점 : 동시성이 높아진다.
  - 단점 : deadlock이 발생할 수 있다.
    - [이전에 deadlock에 대해 정리한 내용](https://github.com/by-gramm/TIL/blob/master/computer_science/deadlock.md)

<br>

#### ReentrantLock

- 객체에 적용된 synchronized 키워드처럼 동작한다.
- 하지만 동기화 블록과 달리 명시적인 locking과 unlocking을 필요로 한다.
- Problem : 임계 영역에서 예외가 발생하면 unlock() 메소드가 호출되지 않는다.
  - 아래 코드의 someOperation() 메소드 내에서 예외가 발생하면 스레드가 중단되고, Lock을 unlock할 스레드가 없어진다. 이는 deadlock을 발생시키는 전형적인 구조에 해당한다.

```java
public static class MyClass implements Runnable {
    private ReentrantLock lock = new ReentrantLock();
 
    @Override
    public void run() {
        lock.lock();
        someOperation();
        lock.unlock();
    }
 
    private void someOperation() {
        // May throw a RuntimeException
    }
}
```

- Solution : try 블록에 임계 영역 코드를, finally 블록에 unlock() 메소드를 넣는다.

```java
public static class MyClass implements Runnable {
    private ReentrantLock lock = new ReentrantLock();
 
    @Override
    public void run() {
        lock.lock();
        
        try {
            someOperations();
        }
        finally {
            lock.unlock();  // 예외가 발생하더라도 반드시 실행된다!
        }
    }
 
    private void someOperation() {
        // May throw a RuntimeException
    }
}
```

- ReentrantLock을 테스트하기 위한 메소드들
  - `getQueuedThreads()`
    - Lock을 기다리는 스레드 목록을 반환한다.
  - `getOwner()`
    - Lock을 가지고 있는 스레드를 반환한다.
  - `isHeldByCurrentThread()`
    - 현재 스레드가 Lock을 가지고 있는지 여부를 반환한다.
  - `isLocked()`
    - 스레드에 Lock이 있는지 여부를 반환한다.
- ReentrantLock의 클래스 생성자
  - `ReentrantLock()`
  - `ReentrantLock(boolean fair)`
    - fair를 true로 주면, Lock의 공정성을 유지할 수 있다. 다시 말하면, 오래 기다린 스레드가 우선적으로 Lock을 획득할 수 있다.
    - 다만 공정성을 유지하기 위해서는 추가 작업이 필요하므로 throughput은 감소한다. 따라서 꼭 필요한 경우에만 fair 옵션을 true로 주어야 한다.
- `lockInterruptibly()`
  - `lock()`과 마찬가지로 Lock을 획득하지만, Lock을 획득하다가 중단된 스레드는 InterruptedException을 발생시킨다. 
  - deadlock을 감지하고 복구하는 감시 장치로 사용할 수 있다.

- `tryLock()` => **중요!**
  - Lock이 사용 가능하다면, Lock을 얻고 true를 리턴한다.
  - Lock이 사용 가능하지 않다면, `lock()`처럼 스레드를 block하는 대신 false를 리턴하고 다음 명령으로 넘어간다.
  - `tryLock(long timeout, TimeUnit unit)`
    - Lock이 사용 가능하지 않은 경우, 바로 false를 리턴하는 대신 인자로 들어온 시간만큼 기다린다.

```java
// lock을 사용한 방식
lockObject.lock();

try {
    useResource();
}
finally {
    lockObject.unlock();
}

// tryLock을 사용한 방식
if (lockObject.tryLock()) {
    try {
        useResource();
    }
    finally {
        lockObject.unlock();
    }
}
else { ... }
```

- 위 코드의 2가지 방식에서, Lock을 다른 스레드가 사용 중인 경우를 생각해보자.
  - lock()을 사용한 방식에서 현재 스레드는 block된다. Lock을 사용 중인 스레드가 Lock을 반환해야 비로소 현재 스레드는 깨어나서 Lock을 얻을 수 있다.
  - tryLock()을 사용한 방식에서 현재 스레드는 block되지 않고, else문의 코드를 실행한다.

<br>

#### ReentrantReadWriteLock

> Read Lock + Write Lock

- synchronized 키워드나 ReentrantLock의 경우, 여러 스레드가 공유 자원을 동시에 읽는 것을 제한한다.
- 읽기 연산의 비중이 높거나, 읽기 연산이 오래 걸리는 경우, 위와 같은 방식은 성능의 문제를 야기한다.
- ReentrantReadWriteLock은 내부적으로 Read Lock과 Write Lock을 가지고 있다.
  - 여러 스레드가 같은 공유 자원에 대해 동시에 read lock을 얻고 읽기 연산을 수행할 수 있다.
- 주의) ReentrantReadWriteLock이 반드시 ReentrantLock보다 성능이 좋은 것은 아니다.

