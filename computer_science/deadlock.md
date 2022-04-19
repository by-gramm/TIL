# Deadlock

> 일련의 프로세스들이 서로가 가진 자원을 기다리며 block된 상태

<br>

### Deadlock 발생의 4가지 조건

- **Mutual exclusion (상호 배제)**
  - 매 순간 하나의 프로세스만이 자원을 사용할 수 있다.

- **No premmption (비선점)**
  - 프로세스는 자원을 스스로 내어놓을 뿐 강제로 빼앗기지 않는다.

- **Hold and wait (보유 대기)**
  - 자원을 가진 프로세스가 다른 자원을 기다릴 때 보유 자원을 내놓지 않고 계속 가지고 있는다.

- **Circular wait (순환 대기)**
  - 자원을 기다리는 프로세스 간에 사이클을 형성한다.

<br>

### 자원 할당 그래프

Deadlock 발생 여부를 확인하기 위한 그래프

![](.\cs.assets\deadlock01.png)![](.\cs.assets\deadlock02.png)

- **Assignment Edge** (R -> P) : 자원이 프로세스에 할당되어 있다.
- **Request Edge** (P -> R) : 프로세스가 자원을 요청했지만 아직 할당받지는 못한 상태다.

[자원 할당 그래프에서 deadlock 판단 기준]

- 그래프에 cycle이 없으면 deadlock이 아니다.
- 그래프에 cycle이 있으면
  - 자원 당 인스턴스가 하나밖에 없다면 (점이 하나) deadlock이다.
  - 자원 당 인스턴스가 여러 개라면, 자원에 연결된 프로세스가 모두 cycle에 포함된 경우만 deadlock이다.

- 첫 번째 그림 : cycle이 없으므로 deadlock이 아니다.

- 두 번째 그림 : cycle이 있고, R2에 인스턴스가 2개씩 있는데, 연결된 프로세스(P1, P2, P3)가 모두 cycle 내에 있으므로 deadlock이다.

- 세 번째 그림 :  cycle이 있고, R1, R2에 인스턴스가 2개씩 있는데, 자원에 연결된 프로세스 중 P2와 P4는 사이클 내에 있지 않으므로 deadlock이 아니다. P2가 작업 완료 후 R1의 자원을 반환하거나, P4가 작업 완료 후 R2의 자원을 반환하면 cycle이 사라질 것이기 때문이다.

<br>

### Deadlock의 해결 방법

아래로 갈수록 약한 방식이다.

- **Deadlock Prevention**
  - 자원 할당시 deadlock의 4가지 조건 중 하나가 만족되지 않도록 한다.
- **Deadlock Avoidance**
  - (자원 요청에 대한 부가적인 정보를 이용해서) deadlock의 가능성이 없는 경우에만 자원을 할당한다.
- **Deadlock Detection and Recovery**
  - deadlock 발생은 허용하되 그에 대한 탐지 루틴을 두어 deadlock 발견시 복구한다.
- **Deadlock Ignorance**
  - deadlock을 시스템이 책임지지 않는다.
  - UNIX를 포함한 대부분의 OS가 채택하고 있는 방식이다.
    - deadlock은 빈번하게 발생하지 않으므로, 이를 미연에 방지하기 위해 많은 오버헤드를 들이는 것이 현재의 시스템에서는 비효율적이기 때문이다.

<br>

### Deadlock Prevention

deadlock의 4가지 조건 중 하나가 만족되지 않도록 한다.

- **Mutual Exclusion** 없애기
  - 애초에 공유할 수 없는 자원인 경우 조건을 없앨 수 없다.
- **Hold and Wait** 없애기
  - 방법 1. 프로세스 시작 시 모든 필요한 자원을 할당받게 한다.
    - 단, 이 방법은 비효율적이다. 한 프로세스가 한참 뒤에 사용할 자원까지 미리 할당받으면, 다른 프로세스는 그 프로세스의 실행이 끝날 때까지 기다려야 하기 때문이다.
  - 방법 2. 자원이 필요할 경우 보유 자원을 모두 놓고 다시 요청하게 한다.
    - 기아 상태(starvation)가 발생할 수 있다.
- **No Preemption** 없애기
  - 더 높은 우선권을 가진 프로세스가 요청한 자원인 경우, 기존에 보유한 자원이 선점된다.
- **Circular Wait** 없애기
  - 모든 자원 유형에 할당 순서를 정하여 정해진 순서대로만 자원을 할당한다.

[문제점]

자주 발생하지도 않을 deadlock 때문에 많은 제약조건을 달아서 비효율적이다. 

<br>

### Deadlock Avoidance

자원 요청에 대한 부가정보를 이용해서 자원 할당이 deadlock으로부터 안전한 경우에만 할당한다.

[2가지 Avoidance 알고리즘]

1) 자원 당 인스턴스가 하나인 경우 : **자원 할당 그래프 알고리즘**
   - 자원 할당 그래프에서 cycle이 생기지 않는 경우에만 요청 자원을 할당한다.

- **Claim Edge** (P -> R) (점선)
  - 프로세스가 한 번이라도 자원을 요청할 수 있음.
- **Request Edge** (P -> R) (실선)
  - 프로세스가 자원을 실제로 요청함.
- **Assignment Edge** (R -> P) (실선)
  - 자원을 프로세스에 할당함.

![](.\cs.assets\deadlock03.png)

세 번째 그림이 deadlock은 아니다. 점선은 평생에 한번 자원을 요청할 수 있는 것을 의미하지, 현재 자원을 요청한 것을 의미하지는 않기 때문이다. 하지만 deadlock avoidance는 deadlock의 가능성이 아예 없는 경우에만, 다시 말해서 점선을 포함해도 cycle이 생기지 않는 경우에만 자원을 할당한다. 그래서 P2가 R2를 요청했을 때, R2를 아무도 가지고 있지 않음에도 P2에 할당하지 않는다. 

<br>

2) 자원 당 인스턴스가 여러 개인 경우 : **Banker's Algorithm (은행원 알고리즘)**

![](.\cs.assets\deadlock04.png)

- Allocation : 현재 프로세스별로 할당된 자원의 수
- Max : 프로세스가 평생 사용하게 될 최대 자원의 수
- Available : 현재 사용 가능한 자원의 수 (총 자원 - 할당된 총 자원)
- Need : 프로세스가 추가로 요청할 자원의 수 (Max - Allocation)

Banker's Algorithm은 프로세스가 최대 요청을 할 것이라고 가정하고, 그것이 현재 가용 가능한  자원으로 충족되는 경우에만 자원을 프로세스에 할당한다. 즉, 해당 프로세스의 `Need <= Available`인 경우에만 그 프로세스에 자원을 할당한다.

- ex1. P0이 (1, 0, 0)을 요청한 경우
  P0의 Need는 (7, 4, 3)이고, Available은 (3, 3, 2)이므로 받아들이지 않는다.
- ex2. P1이 (1, 0, 2)를 요청한 경우
  P1의 Need는 (1, 2, 2)고, Available은 (3, 3, 2)이므로 받아들인다.

위 예제에서는 `<P1, P3, P4, P2, P0>`의 순서로 자원을 모두 할당할 수 있다. 

이처럼 일련의 프로세스의 자원 요청이 safe하게 충족될 수 있는 경우, 이를 **safe sequence**라고 하며, safe sequence가 존재하는 상태를 **safe state**라고 한다.

<br>

### Deadlock Detection and Recovery

deadlock을 탐지하고, deadlock 발견시 복구한다.

**1. Detection**

​	A. 자원 당 인스턴스가 하나인 경우

- 자원 할당 그래프에서 cycle이 있다면 deadlock이 발생함을 알 수 있다.

​	B. 자원 당 인스턴스가 여러 개인 경우

- Banker’s Algorithm과 유사한 방법을 활용한다. safe sequence가 있는지를 검사하여, 없으면 deadlock이 발생함을 알 수 있다.

<br>

**2. Revovery**

- 프로세스 종료시키기
  - 방법 1. deadlock에 연루된 프로세스를 모두 죽인다.
  - 방법 2. deadlock cycle이 없어질 때까지 deadlock에 연루된 프로세스를 하나씩 죽인다.

- 자원 선점(preemption)하기
  - 비용을 최소화할 victim을 선정한다.
  - safe state로 rollback하여 프로세스를 restart한다.
  - starvation 문제
    - 동일한 프로세스가 계속해서 victim으로 선정되는 경우
    - 보완 : cost factor에 rollback 횟수도 같이 고려한다. (일종의 aging 기법)

<br>

### Deadlock Ignorance

Deadlock이 일어나지 않는다고 생각하고 아무런 조치도 하지 않는다.

- deadlock이 매우 드물게 발생하므로 deadlock에 대한 조치 자체가 더 큰 오버헤드일 수 있다.
- 만약 시스템에 deadlock이 발생한 경우 시스템이 비정상적으로 작동하는 것을 사람이 느낀 후 직접 프로세스를 죽이는 등의 방법으로 대처한다.
- UNIX, Windows 등 대부분의 범용 OS가 채택하고 있다.

<br>

### 내용 출처

[KOCW 반효경 교수님 <운영체제> 강의](http://www.kocw.net/home/cview.do?cid=3646706b4347ef09)

https://www.geeksforgeeks.org/deadlock-prevention/