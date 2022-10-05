# 동시성 제어

### Concurrency Control

- **Schedule**

  - 여러 트랜잭션들이 동시에 실행될 때 각 트랜잭션에 속한 연산들의 실행 순서

  - 단, 각 트랜잭션 내의 연산들의 순서는 바뀌지 않는다.

- 여러 트랜잭션이 동시에 실행될 때 작업을 성공적으로 마칠 수 있도록 Schedule을 조절하는 기법
- 동시성 제어를 통해 트랜잭션의 일관성과 고립성을 보장한다.

<br>

### Serializability

- Schedule의 2가지 종류

  - **Serial schedule**
    - 트랜잭션이 순차적으로 실행된다.
  - **Non-serial schedule**
    - 트랜잭션들이 겹쳐서 실행된다.
    - Non-serial schedule은 동시성이 높아지므로, 성능도 높아진다.
    - 대신 예상하지 못한 결과가 나올 수 있다.
- **Conflict**

  - 2개의 연산이 다음의 3가지 조건을 모두 만족하면 conflict에 해당한다.
    1. 서로 다른 트랜잭션에 속한다.
    2. 같은 데이터에 접근한다.
    3. 최소한 하나는 쓰기 연산이다.

  - 둘다 쓰기 연산이면 **write-write conflict**, 하나만 쓰기 연산이면 **read-write conflict**
- **Conflict equivalent**

  - 2개의 schedule이 다음의 2가지 조건을 모두 만족하면 conflict equivalent하다.
    1. 두 schedule은 같은 트랜잭션들을 가진다.
    2. 어떠한 충돌하는 연산의 순서도 양쪽 schedule에서 동일하다.
- **Conflict serializable**
  - 어떤 schedule이 serial schedule과 conflict equivalent함을 의미한다.
  - 주의) 이것이 serializability를 정의하는 유일한 방식은 아니다. **view serializability**도 존재한다. view serializability의 개념은 [다음 링크](https://www.javatpoint.com/dbms-view-serializability)를 통해 이해할 수 있다.
    - view serializable하면 반드시 conflict serializable하지만, 그 반대는 성립하지 않는다.
- conflict serializability를 어떻게 구현하는가?
  - 여러 트랜잭션을 동시에 실행해도 schedule이 conflict serializable하도록 보장하는 프로토콜을 사용한다.

<br>

### Recoverability

- 예시 : 트랜잭션 A가 write한 데이터를 트랜잭션 B가 read한 후 commit을 했다. 그런데 이후 트랜잭션 A에서 문제가 발생하여 rollback을 하고자 한다. 트랜잭션 도중 write한 데이터를 기존 데이터로 돌려놓을 수는 있지만, 문제는 트랜잭션 B가 이미 rollback 이전의 데이터를 읽어서 commit까지 했다는 것이다. 
- 위 예시에서는 rollback을 해도 이전 상태로 온전히 돌아갈 수 없다. 위와 같은 일을 방지하려면 schedule이 recoverability를 가져야 한다.
- **recoverable schedule**
  - schedule 내에서 그 어떤 트랜잭션도 자신이 read한 데이터를 write한 트랜잭션이 먼저 commit/rollback하기 전까지는 commit하지 않는 schedule
  - (내가 읽은 걸 쟤가 썼으면, 쟤가 나보다 먼저 커밋해야 한다.)
- **cascading rollback**
  - 하나의 트랜잭션이 rollback하면, 의존성이 있는 다른 트랜잭션도 rollback하는 방식
  - 문제는 rollback이 연쇄적으로 발생하면 성능에 좋지 않다는 점이다. rollback의 연쇄를 막기 위한 방식이 바로 cascadeless schedule다.
- **cascadeless schedule**
  - schedule 내에서 어떤 트랜잭션도 commit되지 않은 트랜잭션이 write한 데이터는 **읽지 않는 방식**
  - 모든 cascadeless schedule은 recoverable하다.
- **strict schedule**
  - schedule 내에서 어떤 트랜잭션도 commit되지 않은 트랜잭션이 write한 데이터는 **쓰거나 읽지 않는 방식**

<br>

### Lock & 2PL

- **Locking**

  - **write-lock (exclusive lock)**
    - read / write할 때 사용한다.
    - 다른 트랜잭션이 같은 데이터를 read/write하지 못하게 한다.
  - **read-lock (shared lock)**
    - read할 때 사용한다.
    - 다른 트랜잭션이 같은 데이터를 write하지 못하게 한다. (read는 허용한다.)
  - Q. read-lock이 자주 잡히면 write-lock은 실행되지 못하지 않을까?
    - 이러한 현상을 **write-starvation**이라고 한다.
    - 이를 보완하기 위해, 새로운 read-lock을 잡을 수 있더라도 잡지 않고 기다리는 방식 등을 생각해볼 수 있다.
  - 단순 Locking의 문제점
    - serializability를 보장하지 못한다.


- **2PL Protocol (two-phase locking protocol)**
  - 단순 Locking만으로는 serializability를 보장하지 못하는 문제를 해결한다.
  - 트랜잭션에서 모든 lock 연산이 최초의 unlock 연산보다 먼저 수행되도록 한다.
  - lock을 취득만 하는 **expanding phase** => lock을 반환만 하는 **shrinking phase**
  - 단점 : deadlock이 발생할 수 있다.
  - 2PL Protocol의 종류
    - **conservative 2PL**
      - 모든 lock을 취득한 뒤 트랜잭션을 시작한다.
      - deadlock이 발생하지 않지만, 실용적이지 않다.
    - **strict 2PL (S2PL)**
      - strict schedule을 보장하므로, recoverability를 보장한다.
      - 트랜잭션이 commit/rollback될 때 write-lock을 반환한다.
        - 그래야 해당 데이터를 다른 트랜잭션에서 읽거나 쓸 수 없어서, strict schedule을 보장할 수 있기 때문이다.
    - **strong strict 2PL (SS2PL)**
      - strick 2PL과 달리, read-lock 또한 트랜잭션이 commit/rollback될 때 반환한다.
  

<br>

### MVCC (multi-version concurrency control)

- Lock 기반 동시성 제어의 문제점

  - 데이터에 쓰기 연산을 할 때, write-lock이 걸리므로 다른 트랜잭션은 해당 데이터를 읽지도 못한다. 따라서 성능이 비교적 떨어진다.
  - 이를 해결하기 위해 등장한 것이 바로 MVCC다.

- MVCC의 동작 방식

  - read와 write가 서로를 block 하지 않는다.	
    - 따라서 Lock 기반 동시성 제어가 가진 성능 문제를 개선한다.
  - 데이터를 읽을 때 **특정 시점 기준**으로 가장 최근에 commit된 데이터를 읽는다.
    - 이때 특정 시점은 isolation level에 따라 달라진다.
      - `Read Committed` => read하는 시간을 기준으로 직전에 commit된 데이터를 읽는다.
      - `Repeatable Read` => 트랜잭션 시작 시간을 기준으로 직전에 commit된 데이터를 읽는다.
    - 이를 위해 데이터 변화 이력을 관리한다. 따라서 추가적인 저장 공간을 사용한다.

- mySQL의 **Locking Read**

  - MVCC에서는 read와 write가 서로를 block하지 않기 때문에, 동시성 문제가 발생한다.

  - MySQL에서는 locking read 구문을 통해 이를 해결할 수 있다.

  - **SELECT ... FOR UPDATE**

    - 해당 데이터에 write-lock을 건다. (트랜잭션 commit시 lock 해제)

  - **SELECT ... FOR SHARE**

    - 해당 데이터에 read-lock을 건다. (트랜잭션 commit시 lock 해제)

  - 사용 예시

    ```mysql
    SELECT name FROM user WHERE age > 20 FOR UPDATE;
    
    SELECT name FROM user WHERE age > 20 FOR SHARE;
    ```

  - mySQL에서 isolation level을 `Serializable`로 설정하면, 모든 select문이 **SELECT ... FOR SHARE**문처럼 동작한다. 모든 읽기 연산에 read-lock을 거는 셈이므로, 사실상 MVCC라기보다는 lock 기반 동시성 제어라고 볼 수 있다.

<br>

### 참고 자료

- 유튜브 '쉬운코드' 채널의 동시성 제어 관련 영상들

  - schedule과 serializability : https://www.youtube.com/watch?v=DwRN24nWbEc

  - recoverability : https://www.youtube.com/watch?v=89TZbhmo8zk

  - LOCK 기반 동시성 제어 : https://www.youtube.com/watch?v=0PScmeO3Fig

  - MVCC 1부 : https://www.youtube.com/watch?v=wiVvVanI3p4

  - MVCC 2부 : https://www.youtube.com/watch?v=-kJ3fxqFmqA

- write-starvation 현상에 대해 다룬 글

  - https://blog.seulgi.kim/2018/12/rwlock.html

- View Serializability 개념을 설명한 글

  - https://www.javatpoint.com/dbms-view-serializability
