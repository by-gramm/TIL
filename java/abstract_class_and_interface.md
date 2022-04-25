# 추상클래스와 인터페이스



### 추상 클래스

- 메서드 = 선언부 + 구현부
- **추상 메소드**
  - 선언부만 작성한 메소드 (메소드명 앞에 `abstract` 키워드)
  - 추상 메소드에서 구현부를 작성하면 오류가 발생한다.
- **추상 클래스**
  - 추상 메소드를 하나 이상 포함하는 클래스 (클래스명 앞에 `abstract` 키워드)
    - 단, 추상 클래스에는 일반 메소드도 포함될 수 있다.
  - 추상 메소드를 포함하므로, 인스턴스화해서 사용할 수 없다.

```java
// 추상 클래스
abstract class Person {
    // 추상 메소드
    public abstract int getAge();
}
```

- 추상 클래스를 사용하는 이유 = **상속의 강제**

  - 추상 클래스를 `extends` 키워드로 상속 받은 자식 클래스에서 추상 메서드의 구현부를 완성하도록 한다.

  - Q. 상속을 강제하면 좋은 이유는?
  - 여러 클래스의 공통 부분을 추상 클래스에서 관리하기 때문에, 코드 중복이 줄어들며 유지보수가 쉬워진다.

```java
public abstract class Shape 
{
    public int color;
    
    // 추상 메소드
    public abstract float getArea();
}

public class Circle extends Shape {
    private int r;
    
    // 생성자 메서드 생략
    
    @Override
    public float getArea() {
        return 3.14f * r * r;
    }
}

public class Rectangle extends Shape {
    private int width;
    private int height;
    
    // 생성자 메서드 생략
    
    @Override
    public float getArea() {
        return width * height;
    }
}
```

<br>

### 인터페이스

- 추상 클래스가 미완성 설계도라면, 인터페이스는 기본 설계도

- **추상 메소드와 상수**만을 멤버로 가질 수 있다.

  - 모든 멤버 변수는 `public static final`이어야 하며, 이는 생략 가능하다.

  - 모든 메소드는 `public abstract`이어야 하며, 이는 생략 가능하다.

- 추상 클래스와 마찬가지로 추상 메소드를 포함하므로, 인스턴스화해서 사용할 수 없다.

- 인터페이스를 `implements` 키워드로 구현한 객체는 반드시 인터페이스의 모든 메소드를 구현해야 한다.

- cf) Java 8부터는 인터페이스에 **default 메소드**를 사용할 수 있다.

  - default 메소드는 구현부를 작성할 수 있으며, 인터페이스를 사용하는 객체가 반드시 구현하지 않아도 된다.

```java
public interface Person {
    public abstract String eat();
    public abstract String sleep();
    
    // 디폴트 메소드 => 구현부 작성 가능 & 구현 클래스(Kim)에서 구현할 필요 X
    default String sayHello() {
        return "안녕하세요";
    }
}

public class Kim implements Person {
    private String name;
    
    @Override
    public String eat() {
        return "하루 3끼";
    }
    
    @Override
    public String sleep() {
        return "8시간 숙면";
    }
}
```

- 인터페이스를 사용하는 이유 = **객체의 같은 동작을 보장**
  - ex. `talk()` 추상 메소드를 가지는 Talkable 인터페이스를 구현한 객체는 모두 `talk()` 메소드를 구현해야 한다.
  - 선언부와 구현부를 분리하기 때문에 변경하기 쉬운 유연한 설계가 가능하다.
  - 또한 표준화가 가능하다. (프로젝트 규모가 큰 경우 특히 중요)

``` java
interface Talkable {
    public void talk();
}

class Parrot implements Talkable {
    public void talk() {
        System.out.println("I am parrot!");
    }
}

class Human implements Talkable {
    public void talk() {
        System.out.println("I am human!");
    }
}
```

<br>

### 인터페이스와 다형성

- **다형성 (polymorphism)**
  - 같은 인터페이스를 통해 다른 타입의 객체에 접근할 수 있는 성질
- 인터페이스를 구현한 클래스 인스턴스의 자료형을 인터페이스로 지정할 수 있다.
  - `class C implements I`인 경우,  `I obj = new C()`가 가능하다는 것이다.
  - 이를 통해, 다형성을 보장할 수 있다.
  - 아래 코드의 `Printable c = new AdvancedPrint();` 부분에서, Printable은 인터페이스이므로, `Printable c = new RealCal();`로 교체할 수 있다. 같은 인터페이스로 다른 클래스의 객체에 접근할 수 있는 것이다.

```java
// 코드 출처 : https://opentutorials.org/module/4872/28715

interface Calculable {
    double PI = 3.14;
    int sum(int v1, int v2);
}

interface Printable {
    void print();
}

class RealCal implements Calculable, Printable {
    public int sum(int v1, int v2) {
        return v1+v2;
    }
    public void print() {
        System.out.println("This is RealCal!!");
    }
}

class AdvancedPrint implements Printable {
    public void print() {
        System.out.println("This is RealCal!!");
    }
}

public class InterfaceApp {
    public static void main(String[] args) {
        // Printable c = new RealCal();로 교체 가능!
        Printable c = new AdvancedPrint();
        c.print();
    }
}
```

<br>

### 추상 클래스 vs 인터페이스

- 추상 클래스와 인터페이스의 가장 큰 차이는 **다중 상속/구현 가능 여부**다.
  - 추상 클래스(를 포함한 모든 클래스)는 다중 상속이 불가능하다.
  - 인터페이스는 다중 구현이 가능하다.
- Q. 클래스는 왜 다중 상속이 불가능할까?
- 한 클래스가 2개의 클래스를 상속받았는데, 두 클래스에 이름이 같은 메소드/변수가 있는 경우, 둘 중 어떤 메소드/변수를 사용해야 할지 알 수 없기 때문이다.

```java
abstract class A {
    public abstract void introduce();
}

class B extends A {
    @Override
    public void introduce() {
        System.out.println("저는 B입니다.");
    }
}

class C extends A {
    @Override
    public void introduce() {
        System.out.println("저는 C입니다.");
    }
}

// 실제로는 아래와 같은 다중 상속이 불가능함!
class D extends B, C {
    // 생략
}
    
D drake = D();
// B, C 중 누구의 introduce()를 상속받아야 하는지 알 수 없음!
drake.introduce();  
```

- 참고) Python의 경우 다중 상속이 가능하다.
  - 여러 클래스를 상속받은 경우, 먼저 상속받은 클래스의 메소드가 우선권을 가진다. 
  - 그에 따라, 아래 예제에서는 C()의 인스턴스는 A의 introduce()를 실행하게 된다.
  - Python은 **MRO (Method Resolution Order)**를 통해 메소드 실행 순서를 지정함으로써, 다이아몬드 상속 문제를 해결한다.

```python
class A:
    def introduce(self):
        print('저는 A입니다.')

class B(A):
    def introduce(self):
        print('저는 B입니다.')

class C(A):
    def introduce(self):
        print('저는 C입니다.')

# B를 먼저 상속받았으므로, B의 메소드가 C의 메소드보다 우선권을 가진다.
class D(B, C):
    pass

drake = D()
drake.introduce()  # 저는 B입니다.
```

- Q. 인터페이스는 왜 다중 구현이 가능할까?

  - 인터페이스의 모든 메소드는 추상 메소드다. 

  - 한 클래스가 구현한 두 인터페이스에 이름이 같은 추상 메소드가 있는 경우, 클래스에서 해당 메소드를 구현하면 문제가 발생하지 않는다. **둘 중 하나를 상속받는 것이 아니라, 두 추상 메소드를 동시에 구현하는 것이기 때문이다.**

- Q. 두 인터페이스에 이름이 같은 상수가 존재하면?

  - 이 경우에는 상수를 그대로 사용하면 충돌이 발생한다. 
  - 따라서 `인터페이스.상수명`과 같이 어떤 인터페이스의 상수인지를 명시해야 한다.

```java
interface NCT {
    int DEBUT_YEAR = 2016;
}

interface SuperM {
    int DEBUT_YEAR = 2019;
}

public class Mark implements A, B {
    public void getDebutYear() {
        // 아래와 같이 쓰면 두 클래스 중 어떤 클래스의 DEBUT_YEAR인지 알 수 없다.
        // System.out.println(DEBUT_YEAR);
        
        System.out.println(NCT.DEBUT_YEAR);  // 2016
    }
}
```

<br>

### 참고 자료

https://opentutorials.org/course/1223/6062

https://opentutorials.org/course/1223/6063

https://opentutorials.org/module/4872/28715

https://myjamong.tistory.com/150

https://velog.io/@yeonu/%ED%8C%8C%EC%9D%B4%EC%8D%AC-%ED%81%B4%EB%9E%98%EC%8A%A4-%EC%83%81%EC%86%8D#%EB%A9%94%EC%84%9C%EB%93%9C-%ED%83%90%EC%83%89-%EC%88%9C%EC%84%9C-%ED%99%95%EC%9D%B8%ED%95%98%EA%B8%B0

https://stackoverflow.com/questions/32881556/java-7-interfaces-and-name-clashing
