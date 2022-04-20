# Synchronization

> 여러 프로세스/스레드를 동시에 실행해도 공유 데이터의 일관성을 유지하는 것



### 동기화의 필요성

- **race condition (경쟁 상태)** 
  - 여러 프로세스/스레드가 동시에 같은 데이터를 조작할 때 타이밍이나 접근 순서에 따라 결과가 달라질 수 있는 상황

- **critical section (임계 영역)**
  - 공유 데이터에 접근하는 코드
  - race condition을 막기 위해서는 프로세스/스레드가 critical section에 진입하는 것을 제한해야 한다.

<br>

### 동기화 문제의 해결 방법

- **스핀 락(spin lock)**

  - critical section에 들어갈 수 있을 때까지 루프를 돌면서 진입을 시도하는 방식

  - 기다리는 동안 CPU를 낭비한다.

- **뮤텍스(mutex)**
  - mutual exclusion
  - critical section에 들어갈 수 있을 때까지 휴식하며 기다리는 방식
  - critical section에 들어간 프로세스/스레드가 **Lock**을 걸면, 다른 프로세스/스레드는 **Unlock** 상태가 될 때까지 기다린다.

- **세마포어(semaphore)**
  - critical section에 들어가는 프로세스/스레드의 개수를 제한하는 방식
    - 뮤텍스와 달리, 여러 프로세스/스레드가 동시에 critical section에 들어갈 수도 있다.
    - 뮤텍스는 이진 세마포어다.
  - `wait(S)` 연산 : 조건을 만족할 때까지 기다리게 하는 연산
  - `signal(S)` 연산 : 기다리는 프로세스를 깨우는 연산
  - signal 연산과 wait 연산을 이용하여 순서를 정해줄 때 사용할 수 있다.
    - process A 이후 process B가 수행되어야 하는 경우
    - process B 앞에 wait() 연산을, process A 앞에 signal() 연산을 둔다.
    - process A 수행 이후 signal() 연산을 통해 기다리던 process B가 수행된다.

**[뮤텍스 vs 세마포어]**

- 뮤텍스는 세마포어와 달리, 1개의 프로세스/스레드만 critical section에 접근 가능하다.
- 뮤텍스는 Lock을 건 스레드만 Lock을 해제할 수 있다. 반면 세마포어는 `signal()` 연산을 통해 Lock을 걸지 않은 스레드도 Lock을 해제할 수 있다.

<br>

### 참고 출처

https://www.youtube.com/watch?v=gTkvX2Awj6g&ab_channel=%EC%89%AC%EC%9A%B4%EC%BD%94%EB%93%9C

[KOCW 반효경 교수님 <운영체제> 강의](http://www.kocw.net/home/cview.do?cid=3646706b4347ef09)