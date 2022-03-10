# 트랜잭션

>  데이터베이스 시스템에서 병행 제어 및 회복 작업 시 처리되는 작업의 논리적 단위

### 트랜잭션의 연산

- `commit`
  - 트랜잭션이 정상적으로 처리된 경우, 이 처리과정을 DB에 저장한다.
- `rollback`
  - 트랜잭션의 처리 과정에서 문제가 발생한 경우, 변경사항을 취소한다.
  - 트랜잭션의 **원자성**을 위해, 트랜잭션에서 이미 정상적으로 처리된 부분을 모두 취소한다.

<br>

### 트랜잭션의 특징 - ACID

**원자성(Atomicity)**

- 원자(atom) = a(부정) + tomos(쪼갬) => '더 이상 쪼갤 수 없다'
- 트랜잭션은 DB에 모두 반영되거나, 전혀 반영되지 않아야 한다.
- Q. 원자성을 어떻게 보장하는가?
  - `rollback segment` : 트랜잭션 진행시 데이터가 변경될 때 이전 데이터를 저장하는 공간
  - 트랜잭션 처리 과정에서 문제가 발생한 경우, `rollback` 연산을 수행하여 트랜잭션을 수행하기 이전 상태로 되돌린다.
- Q. 트랜잭션이 아무리 길어도 반드시 전부 초기화해야 하는가?
  - `save point`를 지정하면, 이후 rollback시 save point 이후에 수행한 작업만 초기화할 수 있다.

**일관성(Consistency)**

- 트랜잭션이 완료된 후 DB가 일관성을 유지해야 한다. 
- 트랜잭션 수행 전/후에 데이터 모델의 모든 제약 조건(기본 키, 외래 키, 도메인, 도메인 제약조건 등)을 만족하도록 해야 한다.
- Q. 일관성을 어떻게 보장하는가?
  - `trigger` : 테이블에 대한 이벤트에 반응해 자동으로 실행되는 작업
  - 아래 mysql 코드를 예시로 살펴보자. account 테이블의 amount 필드의 경우, 값이 0 ~ 100 사이어야 한다는 제약 조건이 있다. 따라서 0보다 작거나 100보다 큰 값이 들어오게 되면, 일관성이 유지될 수 없다. 그래서 아래 코드에서는 TRIGGER문을 통해 account 테이블에서 UPDATE문이 실행되는 경우, UPDATE문 실행 전에 amount 필드의 값을 0~100 이내로 맞추도록 했다.

```mysql
mysql> delimiter //
mysql> CREATE TRIGGER upd_check BEFORE UPDATE ON account
       FOR EACH ROW
       BEGIN
           IF NEW.amount < 0 THEN
               SET NEW.amount = 0;
           ELSEIF NEW.amount > 100 THEN
               SET NEW.amount = 100;
           END IF;
       END;//
mysql> delimiter ;

(코드 출처: https://dev.mysql.com/doc/refman/8.0/en/trigger-syntax.html)
```

**고립성(Isolation)**

- 트랜잭션은 서로 간섭할 수 없어야 한다.
- 둘 이상의 트랜잭션이 병행 처리(concurrent processing)되는 경우, 실행 중인 트랜잭션이 완료되기 전에, 해당 트랜잭션의 데이터를 다른 트랜잭션에서 참조할 수 없어야 한다. 
- **Lock**을 설정함으로써 고립성을 제어할 수 있다. 이때 주의해야 할 것은 고립성을 완전히 보장하는 것이 꼭 좋지는 않다는 점이다.
- 완벽한 고립성 = 둘 이상의 트랜잭션이 병행 처리될 때의 최종 결과가 하나씩 연속해서 처리될 때의 최종 결과와 동일
- Q. 완벽한 고립성을 어떻게 보장하는가?
  - 트랜잭션 격리 수준을 `Serializable`으로 설정한다. (아래에서 설명할 것이다.)
- Q. 그럼 `Serializable`로 통일하면 좋은 거 아닌가?
  - 꼭 그렇지는 않다. 트랜잭션 격리 수준이 높아질수록 고립성은 보장되지만 동시성(concurrency)이 낮아져 DB의 성능은 저하될 수 있기 때문이다. 따라서 상황에 맞게 트랜잭션 격리 수준을 설정해야 한다.


> 참고) 동시성(concurrency) vs 병행성(parallelism)
>
> - concurrency는 하나의 코어가 여러 일을 동시에 하는 것이다. 일의 주체인 코어가 하나이므로, A => B => C를 번갈아가며 한다.
> - parallelism은 멀티 코어가 각자 자기 일을 하는 것이다. concurrency가 한 사람의 멀티 태스킹이라면, parallelism은 애초에 여러 사람이 동시에 일하는 것으로 이해할 수 있다.

- **트랜잭션 격리 수준**
  - `Read Uncommitted`
    - 말 그대로 커밋되지 않은, 변경 중인 데이터를 읽을 수 있음을 의미한다. 
    - lock 자체를 걸지 않아 트랜잭션 고립성을 보장하지 못하므로 거의 사용하지 않는다.

  - `Read Committed`
    - 커밋된 데이터만 읽을 수 있다. 이를 위해 커밋된 값과 트랜잭션 진행 중인 값을 따로 보관하여, 전자만 읽기를 허용한다.
    - 커밋된 데이터만 덮어쓸 수 있다. 이를 위해 행 단위로 Lock을 사용하여, 같은 데이터를 수정한 트랜잭션이 끝날 때까지 대기한다.

  - `Repeatable Read`
    - 트랜잭션이 같은 데이터를 여러 번 읽을 때 같은 데이터를 읽는 것이 보장된다. 읽는 시점에 특정 버전에 해당하는 데이터만 읽게 하는 등의 방식으로 구현할 수 있다.
    - 트랜잭션 내의 데이터를 다른 사용자가 수정할 수 없다.

  - `Serializable`
    - Serializable 격리 수준을 가진 트랜잭션 내의 데이터는 다른 트랜잭션에서 접근할 수 없다.
    - 성능이 떨어지므로 일반적으로 많이 사용하지 않는다.
  - 풀어서 정리하면 다음과 같다. `Read Uncommitted`는 커밋되지 않은 데이터를 읽을 수 있다는 문제를 가진다. 이를 해결한 것이 `Read Committed`다. 하지만 이 수준에서도 여전히 읽는 동안 데이터가 변경되어, 반복 가능한(repeatable) 읽기가 불가능한 문제가 있을 수 있다.  그래서 트랜잭션이 같은 데이터를 반복해서 읽더라도 같은 데이터를 읽도록 한 것이 `Repeatable Read`다. 그런데 이 수준에서도 여전히 문제가 발생할 수 있다. 반복 가능한 읽기를 보장해야 하므로 트랜잭션에 해당하는 데이터를 변경할 수는 없지만, 새로운 데이터를 추가/삭제할 수는 있기 때문이다. 트랜잭션 A의 수행 중 트랜잭션 B에서 새로운 데이터를 추가/삭제하면, 트랜잭션 A는 트랜잭션 도중 바뀐 데이터를 읽게 된다. 이를 **Phantom Read**라고 하며, 이와 같은 문제를 해결하기 위한 것이 `Serializable`이다. 이 단계에서는 새로운 데이터를 추가/삭제하는 것도 불가능하다.


**지속성(Durability)**

- 트랜잭션의 결과는 영구적으로 반영되어야 한다.

<br>

#### 참고 출처

https://www.youtube.com/watch?v=poyjLx-LOEU

https://victorydntmd.tistory.com/129

https://fauna.com/blog/introduction-to-transaction-isolation-levels

https://dev.mysql.com/doc/refman/8.0/en/trigger-syntax.html

https://gyoogle.dev/blog/computer-science/data-base/Transaction.html
