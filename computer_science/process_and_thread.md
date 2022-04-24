# 프로세스와 스레드

### 멀티 프로세스

- **프로세스**
  - 메모리 상에서 실행 중인 프로그램
- 여러 프로세스가 동시에 실행되는 처리 방식
  - 이때 주의할 점은, 프로세스가 **동시에(concurrently)** 실행된다는 것이 여러 프로세스가 병렬적으로 실행되는 것이 아니라, context switching을 통해 짧은 시분할로 번갈아가며 CPU에 적재됨을 의미한다는 점이다.
- 각 프로세스는 독립적이기에, **IPC**를 통해서 통신해야 한다.
- context switching의 비용이 크다.
- 공유하는 자원이 없기에, 동기화 작업이 필요하지 않다.

<br>

### 멀티 스레드

- **스레드**
  - 프로세스 내에서 나누어진 실행 단위
- 프로세스 내에서 여러 스레드가 동시에 실행되는 처리 방식
- 각 스레드는 stack 영역을 제외한 code, data, heap 영역을 공유한다.

  - 따라서 통신 비용이 절감되며, 메모리를 효율적으로 사용한다.
- 또한 프로세스에 비해 context switching 비용이 작다.
- 단, 자원을 공유하기 때문에 동기화 작업이 필요하다.

<br>

### PCB와 TCB

- 멀티 프로세스 방식에서, CPU 제어권을 프로세스 A에서 프로세스 B로 넘기는 context switching은 아래의 단계로 이루어진다.
  - Step01. 프로세스 A의 문맥 정보를 프로세스 A의 PCB에 저장한다.
  - Step02. 프로세스 B의 문맥 정보를 프로세스 B의 PCB에서 읽어온다.
  - Step03. 프로세스 B에 CPU 제어권을 부여한다.
- **PCB(Process Control Block)**에는 아래와 같은 정보들이 저장된다.
  - Program Counter
    - 실행될 다음 명령어의 주소를 저장한다.
  - 프로세스 번호(PID), 프로세스 상태, 포인터
  - 레지스터, 메모리 제한, 열린 파일 목록 등
- 멀티 스레드 방식에서, 스레드 간의 context switching시 TCB에 스레드의 문맥 정보를 저장한다.
- **TCB(Thread Control Block)**에는 아래와 같은 정보들이 저장된다.
  - Program Counter
    - 실행될 다음 명령어의 주소를 저장한다.
  - 포인터 (스레드가 포함된 프로세스를 가리키는 포인터)
  - 스레드 ID, 스레드 상태, 레지스터 등
- thread context switching이 발생하는 경우, thread의 문맥 정보만 변경하면 된다. 
- 반면 process context switching이 발생하는 경우, thread의 문맥 정보와 process의 문맥 정보를 모두 변경해야 한다.
- process는 thread와 달리 공유하는 영역이 없으므로, context switching시 변경해야 할 문맥 정보도 훨씬 많다.
- 따라서 process context switching의 오버헤드가 훨씬 크다.



<br>

### 멀티 코어

- 여러 코어에서 병렬적으로 프로세스/스레드가 실행되는 방식

- 멀티 프로세스와 멀티 스레드가 **동시성(concurrency)**의 개념이라면, 멀티 코어는 **병렬성(parallelism)**의 개념에 해당한다.

<br>

### 참고 자료

https://www.youtube.com/watch?v=1grtWKqTn50&ab_channel=%EC%9A%B0%EC%95%84%ED%95%9CTech