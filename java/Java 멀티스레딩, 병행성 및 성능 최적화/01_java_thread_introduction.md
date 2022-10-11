## 스레드 생성

#### Thread 클래스

- Thread 클래스는 모든 스레드 관련 기능을 캡슐화한다.

#### 스레드를 생성하는 2가지 방법

- 방법 1 :  Runnable 인터페이스 구현 후 새 Thread 객체에 인자로 전달

```java
Thread thread = new Thread(new Runnable() {
    @Override
    public void run() {
        // 스레드에서 실행될 코드
    }
});
```

- 자바 8 이상에서는 lambda를 활용하여 보다 간단하게 표현 가능하다.

```java
Thread thread = new Thread(() -> {
    // 스레드에서 실행될 코드
});
```

- 방법 2 : Thread 클래스 상속 받은 클래스 생성 후, 해당 클래스의 인스턴스 생성
  - Thread 클래스는 Runnable 인터페이스를 구현한다.

```java
public static void main(String[] args) {
    Thread thread = new newThread();
}

private static class NewThread extends Thread {
    @Override
    public void run() {
    // 스레드에서 실행될 코드
    }
}
```

#### Thread 클래스의 메서드

- `start()` : 스레드 실행
- `setName(String name)` : 스레드 이름 설정
- `setPriority(int newPriority)` : 스레드 우선순위 설정

- `setUncaughtExceptionHandler()` : 예상할 수 없는 exception 처리 핸들러
  - 스레드 내에서 발생한 예외가 어디서도 캐치되지 않으면 핸들러가 호출된다.

```java
thread.setUncaughtExceptionHandler((t, e) -> {
    System.out.println("에러 발생 스레드 : " + t.getName());  // t: thread
    System.out.println("에러 메시지 : " + e.getMessage());   // e: Throwable
});
```

- 그 외 `sleep`, `interrupt`, `join` : [다음 링크](https://github.com/by-gramm/java8study/tree/master/src/main/java/me/bygramm/java8study/Ch06#java-%EB%8F%99%EC%8B%9C%EC%84%B1-%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D)를 참고

<br>

## 스레드 종료

- 스레드 종료가 필요한 경우
  1. 스레드는 아무 일도 하지 않을 때도 리소스를 사용한다. 따라서 스레드가 할 일을 끝냈다면, 스레드가 사용하는 리소스를 정리해야 한다.
  2. 스레드가 오작동하면, 스레드를 종료시켜야 한다.
  3. 애플리케이션 자체를 끝내려면, 먼저 스레드를 종료시켜야 한다.
- `sleep(long millis)` / `sleep(long millis, long nanos)`
  - n밀리초만큼 스레드를 일시정지 상태로 만든다.
- `interrupt()`
  - 스레드가 **일시 정지** 상태에 있을 때 InterruptedException을 발생시킨다.
    - 일시 정지 상태 : WAITING / TIMED_WAITING / BLOCKED
    - 주의) 일시 정지 상태가 아닐 때는 interrupt() 메소드가 호출되어도 스레드가 종료되지 않는다.
  - 일시 정지 상태가 아닌 경우, 직접 interrupt() 호출 여부를 검사해서 처리해야 한다.
    - How? `isInterrupted()` 메서드의 리턴값이 True면 호출되었음을 알 수 있다.

```java
if (Thread.currentThread().isInterrupted()) {
    System.out.println("interrupt() 호출 확인");
    return 0;
}
```

- **Daemon 스레드**
  - 배경에서 실행되는 스레드
  - 애플리케이션이 종료될 때, JVM은 일반 스레드가 모두 종료될 때까지 기다린다. 반면 데몬 스레드가 실행 중인 경우, 종료를 기다리지 않고 그냥 종료시킨다.
  - ex. 텍스트 편집기의 파일 저장 스레드
- `setDaemon(true)`
  - 스레드를 데몬 스레드로 만든다.

<br>

## 스레드 조정

- 스레드 조정이 필요한 이유
  - 스레드 A의 계산 결과를 스레드 B에서 사용해야 하는 경우를 생각해보자. 이때 스레드 B는 스레드 A의 작업 완료 여부를 알아야 한다. 어떻게 알 수 있을까?
    - 루프문을 돌면서 작업 완료 여부를 계속 확인하는 방법 => 비효율적
    - 더 나은 방법 : 스레드 B를 재운 뒤, 스레드 A가 일을 마치면 스레드 B를 깨운다.
- `join()`
  - 스레드가 종료될 때까지 기다린다.
- `join(long millis, long nanos)`
  - 최대 인자로 보낸 시간만큼 스레드가 종료될 때까지 기다린다.
  - 이를 통해 특정 스레드가 완료되는 데 지나치게 오랜 시간이 걸리는 상황에 대비할 수 있다.
- 아래 코드에서는 (base1^power1 + base2^power2)의 값을 구하는데, '+' 앞뒤의 계산식을 각각 다른 스레드에서 계산한 뒤, 두 계산값을 합친다. 이때 두 값을 합치려면, 각각의 스레드에서 계산이 끝났음을 알아야 한다. 이를 위해 join() 메소드를 사용하여, 두 스레드가 종료될 때까지 기다린 이후, 두 스레드의 계산 결과를 합쳤다. 이와 같이 스레드 조정을 위해 join() 메소드를 활용할 수 있다.

```java
public BigInteger calculateResult(int base1, int power1, int base2, int power2) {
    
    PowerCalculatingThread thread1 = new PowerCalculatingThread(base1, power1);
    PowerCalculatingThread thread2 = new PowerCalculatingThread(base2, power2);

    thread1.start();
    thread2.start();

    try {
        thread1.join();
        thread2.join();
    } catch (InterruptedException e) {
        e.printStackTrace();
    }

    return thread1.getResult().add(thread2.getResult());
}
```

