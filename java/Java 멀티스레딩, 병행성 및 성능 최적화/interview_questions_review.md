# Interview Questions Review

> Udemy의 [<Java Multithreading & Concurrency - Interview Practice Exams>](https://www.udemy.com/course/java-multithreading-concurrency-interview-practice-exams/) 강의의 예제들을 리뷰한 내용을 정리합니다.



#### 스레드의 상태

- **NEW**
  - 스레드가 시작하지 않았다.
- **RUNNABLE**
  - 스레드가 JVM에서 실행 중이다.

- **BLOCKED**
  - 스레드가 monitor lock을 기다리며 blocked된 상태다.
- **WAITING**
  - 스레드가 다른 스레드가 특정 행동을 하기를 **무기한으로** 기다리고 있다.
  - 다음 메소드 중 하나를 호출한 스레드는 WAITING 상태가 된다.
    - `Object.wait()`
    - `Thread.join()`
    - `LockSupport.park()`
- **TIMED_WAITING**
  - 스레드가 다른 스레드가 특정 행동을 하기를 **일정한 시간 동안** 기다리고 있다.
  - 다음 메소드 중 하나를 호출한 스레드는 TIMED_WAITING 상태가 된다.
    - `Object.wait(long)`
    - `Thread.join(long)`
    - `Thread.sleep(long)`
    - `LockSupport.parkNanos(Object, long)`
    - `LockSupport.parkUntil(Object, long)`
- **TERMINATED**
  - 스레드의 작업이 종료되었다.



#### [프로세스 분리(process isolation)](https://en.wikipedia.org/wiki/Process_isolation)

- 운영체제의 역할 중 하나
- 하나의 프로세스가 다른 프로세스에 쓰지 못하게 함으로써, 프로세스를 다른 프로세스로부터 보호한다.



#### 스레드 재시작

- 한번 종료된 스레드는 `start()` 메소드를 호출하더라도 다시 시작할 수 없다.



#### 스레드 풀 구현 클래스

> 모두 ExecutorService 인터페이스의 구현 클래스들이다.

- `ForkJoinPool`
  - 다른 스레드풀 구현 클래스와 달리 **work-stealing**의 개념이 존재하는 스레드풀 구현 클래스
    - 스레드가 다른 바쁜 스레드로부터 작업을 가져올 수 있다.
- `ThreadPoolExecutor`
  - 일반적인 목적으로 사용하는 스레드풀 구현 클래스
- `ScheduledThreadPoolExecutor`
  - 작업을 일정 시간 후에 수행하거나, 일정 시간 간격으로 수행하기 위해 사용하는 스레드풀 구현 클래스



#### 조건 변수

- `void Condition.await()`
  - 다른 스레드가 신호를 보내 깨울 때까지 스레드를 잠들게 한다.
- `void Condition.signal()`
  - 현재 조건 변수에서 기다리는 스레드 중 하나를 깨운다.
- 조건 변수에서 `signal()`로 신호를 보내 깨운 스레드는 lock을 가지고 있는 것이 보장된다.
  - 따라서 `await()`을 호출한 스레드가 lock을 가지고 있지 않으면, **IllegalMonitorStateException**이 발생한다.



#### volatile 키워드

- `volatile` 키워드를 사용하면 모든 스레드가 변수에 대해 일관된(consistent) 값을 보게 된다.

- Atomic 변수는 내부적으로 volatile 키워드를 사용하므로, data race가 발생하지 않는다.
- `final` 변수에 `volatile` 키워드를 사용하면 컴파일 에러가 발생한다.



#### coarse-grained locking vs fine-grained locking

- **coarse-grained locking**
  - 모든 critical section을 하나의 Locking으로 제한한다.
- **fine-grained locking**
  - 각 critical section마다 개별 locking을 건다.
- coarse-grained locking과 달리, fine-grained locking은 deadlock의 가능성이 있다.
- fine-grained locking은 coarse-grained locking보다 많은 메모리를 사용한다. 하지만 힙 사이즈가 매우 작은 경우를 제외하면 locking 기법을 선택하는 데 있어 메모리 크기는 일반적으로 고려하지 않는다.
