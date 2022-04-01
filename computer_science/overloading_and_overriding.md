# 오버로딩과 오버라이딩



### 다형성(polymorphism)

> 같은 인터페이스를 통해 다른 타입의 객체에 접근할 수 있는 성질

- 객체 지향 프로그래밍의 가장 중요한 특징 중 하나
- 자바에서는 오버로딩과 오버라이딩을 통해 다형성을 지원한다.

<br>

### 오버로딩(overloading)

> 같은 이름의 메소드를 매개변수의 개수나 타입을 다르게 지정함으로써 2개 이상 정의하는 것

```java
// 메소드 오버로딩 예시
class Calculator {
    int add(int a) {
        return a;
    }
    
    int add(int a, int b) {
        return a + b;
    }

	String add(int a, int b, int c) {
        int sum = a + b + c;
        return sum.toString();
	}
}
```

- Calculator 클래스에 매개변수가 다른 `add()` 메소드 3개를 정의했다. 
- 주의) 오버로딩이 성립하려면 매개변수의 개수나 타입이 달라야 한다. 매개변수의 개수와 타입은 같고 리턴타입만 다른 경우에는 오버로딩이 성립하지 않는다.

오버로딩의 한 종류인 **생성자 오버로딩**은 생성자 메소드를 2개 이상 정의하는 것을 의미한다.

```java
// 생성자 오버로딩 예시
class Coffee {
    
    public String coffeeName;
    public int coffeePrice;
    
    protected Coffee() {
    }
    
    public Coffee(String name) {
        coffeeName = name;
    }
    
    public Coffee(String name, int price) {
        coffeeName = name;
        coffeePrice = price;
    }
}
```

- Coffee 클래스에 매개변수를 받지 않는 **기본 생성자**를 포함하여 총 3개의 생성자 메소드를 정의했다. 

**참고: 파이썬의 오버로딩**

파이썬에서는 언어 차원에서 오버로딩을 지원하지 않는다. (오버라이딩은 지원한다.) 대신 `MultipleDispatch` 라이브러리를 사용하면 자바와 같이 오버로딩을 사용할 수 있다. 위의 Calculator 클래스를 `MultipleDispatch` 라이브러리를 사용한 파이썬 클래스로 구현하면 아래와 같다.

```python
from multipledispatch import dispatch


class Calculator():
  
    @dispatch(int)
    def add(self, a) {
        return a
    }
    
    @dispatch(int, int)
    def add(self, a, b) {
        return a + b
    }

    @dispatch(int, int, int)
	def add(self, a, b, c) {
        return a + b + c
	}
```

<br>

### 오버라이딩(overriding)

> 상위 클래스나 인터페이스의 메소드를 재정의하는 것

```java
public class Coffee {
    
    public String name;
    public int price;
    
    public void showPrice() {
        System.out.println("커피 가격: " + this.price);
    }
}


public class Americano extends Coffee {
    
    public String origin;
    
    // override
    public void showPrice() {
        super.showPrice();
        System.out.println("커피 종류: 아메리카노");
    }
}
```

- Coffee 클래스를 상속 받은 Americano 클래스에서 `showPrice()` 메서드를 오버라이딩했다.

**자바 @override 어노테이션**

- 해당 메서드가 오버라이딩했음을 컴파일러에게 알린다.

- 오버라이딩한 메서드에 문제가 있는 경우, 컴파일러 에러(good!)가 발생한다. 

