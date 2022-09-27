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

- **process context switching**
  - 다른 프로세스에 속한 스레드 간에 이루어지는 context switching
  - process context switching은 아래의 단계로 이루어진다.
    - Step01. 프로세스 A의 문맥 정보를 프로세스 A의 PCB에 저장한다.
    - Step02. 프로세스 B의 문맥 정보를 프로세스 B의 PCB에서 읽어온다.
    - Step03. 프로세스 B에 CPU 제어권을 부여한다.

- **PCB(Process Control Block)**에는 아래와 같은 정보들이 저장된다.
  - Program Counter
    - 실행될 다음 명령어의 주소를 저장한다.
  - 프로세스 번호(PID), 프로세스 상태, 포인터
  - 레지스터, 메모리 제한, 열린 파일 목록 등
- **thread context switching**
  - 같은 프로세스에 속한 스레드 간에 이루어지는 context switching
  - TCB에 스레드의 문맥 정보를 저장한다.

- **TCB(Thread Control Block)**에는 아래와 같은 정보들이 저장된다.
  - Program Counter
    - 실행될 다음 명령어의 주소를 저장한다.
  - 포인터 (스레드가 포함된 프로세스를 가리키는 포인터)
  - 스레드 ID, 스레드 상태, 레지스터 등
- process context switching vs thread context switching
  - process context switching의 오버헤드가 더 크다.

  - process context switching의 경우, 가상 메모리 주소 관련 처리를 추가로 수행해야 하기 때문이다.
    - MMU가 새로운 프로세스의 메모리를 바라보도록 만든다.
      - MMU : 논리적 주소를 물리적 주소로 변환해주는 장치

    - TLB를 초기화한다. 
      - TLB : 논리적 주소와 물리적 주소를 매핑시킨 값을 저장하는 캐시
      - 단, 프로세스를 식별할 수 있는 ASID를 사용하면 초기화하지 않아도 된다.


<br>

### 멀티 코어

- 여러 코어에서 병렬적으로 프로세스/스레드가 실행되는 방식

- 멀티 프로세스와 멀티 스레드가 **동시성(concurrency)**의 개념이라면, 멀티 코어는 **병렬성(parallelism)**의 개념에 해당한다.

<br>

### 참고 자료

https://www.youtube.com/watch?v=1grtWKqTn50&ab_channel=%EC%9A%B0%EC%95%84%ED%95%9CTech

https://www.youtube.com/watch?v=Xh9Nt7y07FE&ab_channel=%EC%89%AC%EC%9A%B4%EC%BD%94%EB%93%9C