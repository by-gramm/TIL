최범균님의 [<객체 지향 프로그래밍 입문>](https://www.inflearn.com/course/%EA%B0%9D%EC%B2%B4-%EC%A7%80%ED%96%A5-%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D-%EC%9E%85%EB%AC%B8) 강의를 바탕으로 정리한 내용입니다.

<br>

### 들어가며

> 핵심은 변화의 비용을 낮추는 것이다.

- 소프트웨어 제품의 출시 횟수가 증가함에 따라, 코드 한 줄을 추가하는 비용이 증가한다.

- Why?

  1. 코드 분석 시간 증가

  2. 코드 변경 시간 증가

- 소프트웨어의 가치: 변화
  - Jessica Kerr: Software maintenance is not "keep it working like before". It is "**keep being useful in a changing world**"

- **핵심: 변화의 비용을 낮추는 것!**
- How?
  - 패러다임
    - **객체 지향 프로그래밍**, 함수형 프로그래밍, 리액티브 프로그래밍...
  - 코드, 설계, 아키텍처
    - TDD, DDD, SOLID, 클린 아키텍처, MSA
  - 업무 프로세스/문화
    - 애자일, DevOps...

- 객체 지향 프로그래밍은 어떻게 변화의 비용을 낮추는가?
  1. 캡슐화
  2. 다형성(추상화)

<br>

### 객체

> 객체는 기능으로 정의된다.

- **절차 지향 프로그래밍**

  - 여러 프로시저가 같은 데이터를 공유하는 프로그래밍 패러다임
  - 프로시저가 데이터에 직접 접근 가능하다.

- **객체 지향 프로그래밍**

  - 프로시저와 데이터를 객체(Object) 단위로 캡슐화하는 프로그래밍 패러다임
    - 프로시저가 메소드, 데이터가 필드에 해당한다.
  - 어떤 객체의 데이터는 해당 객체의 프로시저만 접근 가능하다.
  - 다른 객체의 데이터에 접근하려면 (데이터에 직접 접근하는 대신) 프로시저를 호출해야 한다.

- 절차 지향 vs 객체 지향

  - 초기 구현은 절차 지향 방식이 더욱 쉽다.
  - 하지만 기능 추가/수정 시 객체 지향 방식이 더 적은 비용이 든다.

- **객체(Object)**

  - 객체는 필드(데이터)가 아니라, 제공하는 **기능으로 정의된다.**

    - ex. 회원 객체: 이름, 나이 등의 필드가 아니라 암호 변경 기능 등의 기능으로 정의됨.
    - 따라서, 아래와 같이 기능이 없는 클래스는 객체라고 보기 어렵다.

    ```java
    @Getter
    @Setter
    public class Member {
        private String name;
        private String id;
    }
    ```

  - 기능은 **메소드(method)**를 이용해서 명세한다.

    - 이름, 파라미터, 결과로 구성

  - 객체와 객체는 기능을 사용해서 연결된다. 이때, 기능을 사용한다는 것은 메소드를 호출함을 의미한다.

- 메시지

  - 메시지를 주고받는다 = 객체와 객체가 상호작용한다

<br>

### 캡슐화

> Tell, Don't Ask 규칙으로 캡슐화한다.

- 데이터와 관련된 기능을 묶고, 기능의 구현을 외부에 감추는 것

- 캡슐화와 은닉화를 구분하기도 하지만, 최근에는 주로 캡슐화에 정보 은닉의 의미까지 포함한다.

- Why?

  1. **Loose Coupling(느슨한 결합도)**

     - 객체 내부 구현을 변경할 때, 해당 객체의 기능에 접근하는 클래스에 영향을 최소화한다.

     - 일반화하면, 변경에 대한 비용을 최소화한다.

  2. 기능에 대한 이해를 높인다.

  ```java
  // 캡슐화 X
  // 멤버십이 REGULAR와 같은지 비교하는 이유를 알려면, 코드의 다른 부분까지 살펴보아야 함.
  if (acc.getMemberShip() == REGULAR) {
  }
  
  // 캡슐화 O
  // 메소드가 계정이 REGULAR 권한을 가졌는지 확인하는 기능을 가진다는 것이 한눈에 파악됨.
  public class Account {
      public boolean hasRegularPermission() {
      }
  }
  
  if (acc.hasRegularPermission()) {
  }
  ```

- 캡슐화를 위한 규칙

  - **Tell, Don't Ask**

    - "rather than asking an object for data and acting on that data, we should instead tell an object what to do" (출처: [Martin Fowler - TellDontAsk](https://martinfowler.com/bliki/TellDontAsk.html))

    ```java
    // 데이터를 가져와서 작업을 수행하기보다는
    if (acc.getMembership() == REGULAR) {
    }
    
    // 객체에게 할 일을 말해주자
    if (acc.hasRegularPermission()) {
    }
    ```

  - **Demeter's Law (디미터 법칙)**

    - Don't Talk to Strangers / Principle of least knowledge

    - 객체의 메소드에서 다른 객체의 메소드를 호출할 때 아래 3가지 중 하나에 해당하는 경우에만 호출해야 한다.

      1. 메소드에서 생성한 객체의 메소드

      2. 파라미터로 받은 객체의 메소드

      3. 필드로 참조하는 객체의 메소드

    ```java
    // X (위의 3가지에 해당하지 않는 Date 객체의 메소드를 호출)
    acc.getExpDate().isAfter(now)
    
    // O
    acc.isExpired()
    acc.isValid(now)
    ```

 <br>

### 추상화

> 공통의 속성과 기능을 정의하여 OCP를 적용한다.

- **다형성(polymorphism)**
  - 하나의 객체가 여러 타입의 기능을 제공하는 것

- **추상화(abstraction)**
  - 데이터나 프로세스 등을 의미가 비슷한 개념이나 의미 있는 표현으로 정의하는 과정
- 추상화의 2가지 방식
  - 특정한 성질
    - ex. 사용자에서 id, name, email을 뽑아서 User 테이블로 추상화
  - 공통 성질(일반화)
    - ex. NCT, IVE에서 공통점을 뽑아서 케이팝 그룹으로 추상화
    - 다형성을 활용한 추상화가 이에 해당한다.

- 타입 추상화
  - 여러 구현 클래스를 대표하는 추상 타입을 도출한다.
    - 흔히 인터페이스 타입으로 추상화한다.
  - 추상 타입을 이용하여 프로그래밍하면 기능의 의도를 드러내면서 구현 내용은 감출 수 있다.

- 추상화 예시

```java
// 1. 구현 클래스 직접 사용

private SmsSender smsSender;
private KakaoPush kakaoPush;
private MailService mailService;

public void cancel(String ono) {
    // 주문 취소 처리
    
    if (pushEnabled) {
        kakaoPush.push(...);
    } else {
        smsSender.sendSms(...);
    }
    mailService.sendMail(...);
}
```

```java
// 2. SMS 전송, 카카오톡 전송, 이메일 발송 => '통지'라는 공통 성질을 가짐
// 공통 성질로 도출한 추상 타입 Notifier 사용

public void cancel(String ono) {
    // 주문 취소 처리
    
    Notifier notifier = getNotifier(...);
    notifier.notify(...);
}

private Notifier getNotifier(...) {
    if (pushEnabled) {
        return new KakaoNotifier();
    } else {
        return new SmsNotifier();
    }
}

// 추상화의 결과, 통지 방식이 변경되더라도 주문을 취소하는 코드는 변경되지 않는다!
```

- 추상화 사용시 주의점
  - 추상화를 할수록 추상 타입이 증가하여, 복잡도가 증가한다.
  - 따라서 실제로 변경/확장이 발생할 때 추상화를 시도하는 것이 좋다.

- **OCP (Open-Closed Principle)**
  - 확장에는 열려 있어야 하고, 변경에는 닫혀 있어야 한다.
  - 기능을 변경하거나 확장하면서도, 해당 기능을 사용하는 코드는 수정하지 않아야 한다.
    - 추상화를 통해 OCP 원칙을 지킬 수 있다.

<br>

### 상속보다는 조립

> Effective Java Item 18 : "Favor composition over inheritance"

- 상속을 통한 기능 재사용의 단점

  1. 상위 클래스의 변경이 어렵다.
     - 상위 클래스의 변경이 모든 하위 클래스에 영향을 줄 수 있기 때문이다.
  2. 클래스가 증가한다.
     - A, B, C, D 기능이 있다고 하자. 이중 A만 사용하는 클래스, A와 B만 사용하는 클래스, B/C/D만 사용하는 클래스 등을 구현하려면 매번 새로운 클래스를 만들어야 한다.
  3. 상속을 오용할 수 있다.

  ```java
  // 상속 오용 예시
  public class Container extends ArrayList<Luggage> {
      private int maxSize;
      private int currentSize;
      
      public Container(int maxSize) {
          this.maxSize = maxSize;
      }
      
      public void put(Luggage lug) throws NoSpaceException {
          if (!canContain(lug)) throw new NoSpaceException();
          super.add(lug);
          currentSize += lug.size();
      }
      
      public boolean canContain(Luggage lug) {
          return maxSize >= currentSize + lug.size();
      }
  }
  
  
  Container c = new Container(10);    // 용량이 10인 컨테이너
  Luggage luggage = new Luggage(8);   // 크기가 8인 수화물
  
  if (c.canContain(luggage)) {
      c.add(luggage);
  }
  
  // 원래 if문이 false가 되어야 하지만, 상속의 오용으로 true가 된다.
  if (c.canContain(luggage)) {
      c.add(luggage);
  }
  ```

  - 수화물을 싣는 만큼 컨테이너의 currentSize를 증가시켜야 한다.
  - 하지만 put() 대신 ArrayList의 add()를 사용하여, 이 부분이 반영되지 않았다.
  - 그래서 용량보다 많은 수화물을 싣는 오류가 발생하게 된다.
  - 이와 같이, 실수할 확률이 높도록 설계하는 것은 좋지 않은 설계이다.

- **조립(Composition)**
  - 상속의 단점을 해결할 수 있다.
  - 여러 객체를 묶어서 더 복잡한 기능을 제공한다.
  - 일반적으로 기능을 사용하고 싶은 클래스의 객체를 멤버 필드에 담아 사용한다.

- 상속 < 조립
  - 상속하기에 앞서 조립으로 풀 수 없는지 검토한다.
  - 진짜 하위 타입인 경우에만 상속을 사용한다.

<br>

### 기능과 책임 분리

> 기능을 분리하고, 분리한 기능을 알맞은 객체에 분배한다.

- 객체지향 설계의 기본은 기능을 분리하고, 분리한 기능을 여러 객체에 분배하는 것이다.
- 클래스나 메소드가 커지면, 절차 지향과 같은 문제가 발생한다.
  - 클래스가 커질수록, 많은 필드를 많은 메소드가 공유한다.
  - 메소드가 커질수록, 많은 변수를 많은 코드가 공유한다.
  - 따라서, 책임에 맞게 코드를 분리해야 한다.

- 책임을 분리하는 4가지 방법
  1. 패턴 적용
     - 전형적인 역할 분리
     - ex. 복잡한 도메인 => Entity, Value, Repository, Service로 분리
     - ex. AOP => 공통 기능을 Aspect로 분리
     - ex. 디자인 패턴으로 역할 분리
  2. 계산 분리
     - 계산하는 부분을 새로운 메소드로 분리한다.
  3. 연동 분리
     - 네트워크, 메시징, 파일 등 외부 연동을 처리하는 코드를 분리한다.
  4. 조건 분기 추상화
     - 연속적인 if-else를 추상화한다.
- 역할 분리의 이점
  - 특정 기능만 테스트하는 것이 쉬워진다.

<br>

### 의존과 DI

> DI를 습관적으로 사용하자

- **의존한다(dependent)**
  - 기능 구현을 위해 다른 구성 요소를 사용하는 것
  - 변경이 전파될 가능성을 내포한다. A가 B에 의존하는 경우, B가 바뀌면 A도 바뀔 가능성이 높아진다.
    - 따라서 순환 의존이 발생하지 않도록 해야 한다.
  - 의존 대상이 많으면 변경 가능성이 커지므로, 의존 대상은 적을수록 좋다.
- 의존 대상을 줄이는 방법
  - 하나의 클래스에 기능이 많은 경우, 기능별로 클래스를 분리한다.
  - 여러 의존 대상을 단일 기능으로 추상화한다.
- 의존 대상 객체를 직접 생성하면, 생성 클래스가 바뀌면 의존하는 코드도 바뀐다.

- 의존 대상 객체를 직접 생성하지 않는 방법
  1. [팩토리 패턴](https://en.wikipedia.org/wiki/Factory_method_pattern#Java), [빌더 패턴](https://en.wikipedia.org/wiki/Builder_pattern)
  2. Dependency Injection
     - 외부에서 의존 객체를 주입하는 방식
     - 생성자 주입 / setter 주입 / 필드 주입
  3. [Service Locator](https://en.wikipedia.org/wiki/Service_locator_pattern)

- **조립기(Assembler)**
  - 조립기에서 객체 생성, 의존 주입을 처리한다.
  - ex. Spring Framework
- DI의 장점
  1. 의존 대상이 바뀔 때, 조립기(설정)만 변경하면 된다.
  2. 의존 객체의 실제 구현 없이 대역 객체를 사용하여 테스트하기 쉽다.

<br>

### DIP

> 저수준 모듈이 고수준 모듈에 의존해야 한다.

- 고수준 모듈
  - 의미 있는 단일 기능을 제공한다.
  - ex. 도면 이미지 저장, 측정 정보 저장
- 저수준 모듈
  - 고수준 모듈의 기능 구현에 필요한 하위 기능을 실제로 구현한다.
  - ex. NAS에 이미지 저장, MEAS_INFO 테이블에 저장
- **DIP(Dependency Inversion Principle)**
  - 고수준 모듈은 저수준 모듈의 구현에 의존하면 안 된다.
    - 인터페이스가 구현 클래스에 의존하면 안 된다.
  - 저수준 모듈이 고수준 모듈에서 정의한 추상 타입에 의존해야 한다.
- Why?
  - 고수준 모듈이 저수준 모듈에 직접 의존하면, 저수준 구현이 바뀔 때 고수준 모듈에 영향을 준다.
- DIP의 장점
  - 고수준 모듈의 변경 없이 저수준 모듈을 변경할 수 있으므로, 유연함을 높인다.
