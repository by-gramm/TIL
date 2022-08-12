# Statement vs PreparedStatement 

> Java에서 SQL 쿼리문을 전달하기 위한 인터페이스

#### Statement

- 쿼리문 실행시마다 `쿼리 문장 분석 => 컴파일 => 실행`의 단계를 거친다.
- SQL문 수행시 매번 컴파일을 하므로, 성능 이슈가 발생한다.
- 실행 중인 SQL문을 확인할 수 있다.

<br>

#### PreparedStatement

- SQL문이 미리 컴파일되어 `PreparedStatement` 객체에 담긴다.
- 이 객체는 캐시에 저장되어, 이후 같은 쿼리문을 효율적으로 반복 사용할 수 있다.
- 변수를 바인딩하기 전에 쿼리의 문법적인 부분을 미리 처리한다. 따라서 SQL Injection을 방지할 수 있다.
  - **SQL Injection**
    - 악의적인 SQL문이 실행되게 하여 DB를 비정상적으로 조작하는 방법
    - ex. 로그인시 비밀번호 입력란에 `'1' or '1'='1'`과 같이 적는다. OR 뒤쪽이 true이므로 해당 조건은 반드시 참이 되어, 비밀번호와 관계없이 조건을 만족하게 된다.

<br>

#### 정리

- PreparedStatement는 객체를 캐시에 담기 때문에 효율적인 재사용이 가능하다.
- PreparedStatement는 SQL Injection을 방지할 수 있다.