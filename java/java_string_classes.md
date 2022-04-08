# Java 문자열 클래스

> String vs StringBuilder vs StringBuffer

### 1. mutable한가?

> String은 **불변(immutable)**, StringBuilder/StringBuffer는 **가변(mutable)**이다.

```java
String name = "java";
name.concat("script");  // javascript
```

- String은 불변 클래스이므로, 값이 변경되지 않는다. 
- `concat` 메서드로 문자열을 더하면, 기존 String 객체의 값이 "javascript"로 변경되는 것이 아니라, "javascript" 값을 가지는 새로운 String 객체가 메모리에 저장되고, 변수 name이 해당 메모리 영역을 가리키게 된다. 
- Q. 기존 String 객체는? 더 이상 참조되지 않기 때문에 **가비지 컬렉션**의 대상이 된다.

```java
StringBuffer name = new StringBuffer("java");
name.append("script");
```

- StringBuffer는 가변 클래스이므로, 값이 변경될 수 있다.
- `append` 메서드로 문자열을 더하면, 기존 StringBuffer 객체의 값이 변경된다.

<br>

### 2. thread-safe한가?

> String/StringBuffer는 **thread-safe하고**, StringBuilder는 **thread-safe하지 않다**.

- **thread-safe**
  - A function is thread-safe *if and only if* it will always produce correct results when called repeatedly from multiple concurrent threads
  - 멀티쓰레드 환경에서, 여러 쓰레드가 동시에 호출해도 항상 correct한 결과가 나온다
  - ex. **HashMap**은 thread-safe하지 않고, **ConcurrentHashMap**은 thread-safe하다.
  - 참고) [트랜잭션의 ACID 중 고립성(Isolation)](https://github.com/by-gramm/TIL/blob/master/computer_science/transaction.md#%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98%EC%9D%98-%ED%8A%B9%EC%A7%95---acid)
- String은 애초에 값이 변하지 않으므로 thread-safe하다.
- StringBuffer는 내부 메서드들에 **synchronized** 키워드가 선언되어 있기 때문에 thread-safe하다. 반면 StringBuilder는 그렇지 않으므로 thread-safe하지 않다.

```java
// https://github.com/frohoff/jdk8u-jdk/blob/master/src/share/classes/java/lang/StringBuffer.java

@Override
public synchronized StringBuffer append(String str) {
    toStringCache = null;
    super.append(str);
    return this;
}
```

```java
// https://github.com/frohoff/jdk8u-jdk/blob/master/src/share/classes/java/lang/StringBuilder.java

@Override
public StringBuilder append(String str) {
    super.append(str);
    return this;
}
```

- 위의 예시 코드는 JDK 8에서 두 클래스가 `append` 메서드를 정의한 부분이다. StringBuffer 클래스의 `append` 메서드에만 synchronized 키워드가 정의된 것을 볼 수 있다.

- StringBuilder는 thread-safe하지 않은 대신, StringBuffer보다 연산 속도가 빠르다. 