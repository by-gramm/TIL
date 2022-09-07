> 스프링 Dependency Injection은 어떻게 동작할까?

### 클래스 정보 조회

- `Class<T>` (클래스 타입)은 리플렉션의 시작이다.

- JVM 파트에서 배운 것처럼, 클래스 로더에서 Loading이 끝나면 해당 클래스 타입의 Class 인스턴스를 생성하여 힙 영역에 저장한다.
- 클래스 타입에 접근하는 방법
  1. `타입.class`
  2. `인스턴스.getClass()`
  3. `Class.forName("FQCN")`
     - FQCN: 클래스가 속한 패키지명을 모두 포함한 이름 (ex. org.example.Book)

```java
// 1. 타입.class
Class<Book> bookClass1 = Book.class;

// 2. 인스턴스.getClass()
Book book = new Book();
Class<? extends Book> bookClass2 = book.getClass();

// 3. Class.forName([FQCN])
Class<?> bookClass3 = Class.forName("me.gramm.Book");
```

**Class<T> API 예시**

- `getFields()`
  - public한 필드 목록 가져오기
- `getDeclaredFields()`
  - 모든 필드 목록 가져오기
- `getMethods()`
  - 모든 메소드 목록 가져오기
- `getConstructors()`
  - 생성자 목록 가져오기
- `getSuperclass()`
  - 상위 클래스 가져오기
- `getInterfaces()`
  - 인터페이스 목록 가져오기
- `getAnnotations()`
  - 애노테이션 목록 가져오기

- `getModifiers()`
  - int형으로 부호화된 제어자(modifier) 목록 가져오기
    - ex. public => 1 / private => 2 / private static final => 26
  - `Modifiers.isPrivate()`과 같이 특정 제어자의 포함 여부를 확인할 수 있다.

<br>

### 어노테이션과 리플렉션

- **메타 어노테이션**
  - 다른 어노테이션에 사용될 수 있는 어노테이션
  - ex. `@Component`는 `@Controller`, `@Service` 등의 어노테이션에 붙으므로, 메타 어노테이션이다.
- 주요 메타 어노테이션
  - **@Retention**
    - 어노테이션의 유지 기간을 지정한다.
    - `SOURCE` / `CLASS` / `RUNTIME`
  - **@Target**
    - 어노테이션이 사용될 수 있는 요소를 지정한다.
    - `TYPE` / `FILED` / `METHOD` / `CONSTRUCTOR` 등
    - Java 8에서 `TYPE_USE`, `TYPE_PARAMETER`가 추가되었다. ([참고](https://github.com/by-gramm/java8study/tree/master/src/main/java/me/bygramm/java8study/Ch07))
  - **@Inherit**
    - 해당 어노테이션을 하위 클래스까지 전달할지 여부를 지정한다.
- 어노테이션은 값을 가질 수 있다.

```java
public @interface NewAnnotation {
    String name();
    int number();
}
```

- 어노테이션이 값을 가지는 경우, 어노테이션 사용시 값을 명시해주어야 한다.

```java
@NewAnnotation(name = "Jeans", number = 100)
```

- 어노테이션의 값에 디폴트값을 부여할 수 있고, 이 경우에는 따로 명시하지 않아도 된다.

```java
public @interface NewAnnotation {
    String name() default "Jeans";
    int number() default 5;
}
```

- 어노테이션은 클래스뿐 아니라 필드나 메소드에도 붙일 수 있다.

**어노테이션 관련 Class<T> API**

- `getAnnotations()`
  - @Inherit으로 상속받은 어노테이션까지 조회
- `getDeclaredAnnotations()`
  - 자기 자신에 붙은 어노테이션만 조회

<br>

### 클래스 정보 수정

실습에 사용할 Book 클래스

```java
public class Book {
    public static String A = "A";
    
    private String B = "B";
 
    public Book() {
    }
 
    public Book(String b) {
        B = b;
    }
 
    private void c() {
        System.out.println("C");
    }
 
    public int sum(int num1, int num2) {
        return num1 + num2;
    }
}
```

- Class 인스턴스 만들기
  - 생성자를 통해서 만들어야 한다.

```java
// 1. 클래스 가져오기
Class<Book> bookClass = Book.class;

// 2. 생성자 가져오기
//    (인자 타입을 넘겨준다. 기본 생성자의 경우 null을 넘겨준다.)
Constructor<?> constructor = bookClass.getConstructor(null);           // 기본 생성자
Constructor<?> constructor2 = bookClass.getConstructor(String.class);  // 인자가 있는 생성자

// 3. 생성자로 인스턴스 생성하기 (생성자 인자를 넘겨준다.)
Book book = (Book) constructor.newInstance();
Book book2 = (Book) constructor.newInstance("myBook");
```

- 필드 값 접근/설정하기
  - 접근 : `Field.get(object)`
  - 설정 : `Field.set(object, value)`

```java
Field a = Book.class.getDeclaredField("A");
// A는 static 필드 => get/set에서 인자로 null을 넘긴다.
System.out.println(a.get(null));
a.set(null, "aChanged");

Book book = new Book();
Field b = Book.class.getDeclaredField("B");
// B는 private => setAccessible(true)로 접근 가능하게 만든다.
b.setAccessible(true);  
// B는 인스턴스 필드 => get/set에서 인자로 인스턴스(book)를 넘긴다.
System.out.println(b.get(book));
b.set(book, "newName");
```

- 메소드 실행하기
  - `메소드.invoke(object, params)`

```java
Method c = Book.class.getDeclaredMethod("c");
c.setAccessible(true);
c.invoke(book);

// 메소드에 매개변수가 있는 경우, 메소드명과 함께 매개변수들의 자료형을 넘긴다.
Method sum = Book.class.getDeclaredMethod("sum", int.class, int.class);
// 인스턴스와 인자들을 넘겨 메소드를 실행시킨다.
sum.invoke(book, 10, 20);
```

<br>

### 리플렉션 정리

- 활용
  - Spring
    - DI
    - MVC 뷰에서 넘어온 데이터를 객체에 바인딩할 때
  - Hibernate
    - @Entity 클래스에 Setter가 없을 때 리플렉션을 사용한다.

- 주의할 점
  - 지나친 사용은 성능 이슈를 야기할 수 있다.
  - 컴파일 타임에 확인되지 않고 런타임 시에만 발생하는 문제를 만들 수 있다.
  - 접근 제한자를 무시할 수 있다.