# 3장 함수


## Better Way 19

> 함수가 여러 값을 반환하는 경우 절대로 네 값 이상을 언패킹하지 말라



- 함수는 원칙적으로 하나의 값만을 반환할 수 있다.

- 하지만 실제로는 여러 값을 리턴하는 것이 가능하다. return 뒤에 여러 값을 적는 경우, 함수가 그 값들을 하나의 튜플로 묶어 반환해주기 때문이다.

  ```python
  def get_ranks(scores):
      scores.sort(reverse=True)
      gold, silver, bronze = scores[0], scores[1], scores[2]
      return gold, silver, bronze
  
  
  current_scores = [10, 60, 50, 80, 90, 30, 40]
  gold, silver, bronze = get_ranks(current_scores)
  print(gold, silver, bronze)
  
  # 90 80 60
  ```

- 하지만 하나의 함수가 4개 이상의 값을 반환하는 것은 좋지 않다. 순서를 혼동하기도 쉬우며, 가독성도 나빠지기 때문이다.
- 만약 함수가 4개 이상의 값을 반환해야 한다면, 경량 클래스나 `namedtuple`을 사용하는 것이 좋다. (=> Better Way 37)

</hr>

## Better Way 20

> None을 반환하기보다는 예외를 발생시켜라



- 파이썬에서는 특별한 경우를 처리하기 위해 `None`를 사용할 수 있다.

  ```python
  def careful_divide(a, b):
      try:
          return a / b
      except ZeroDivisionError:
          return None
  
  # 출처 : [파이썬 코딩의 기술 2판] p.138
  ```

- 그런데 위와 같은 코드에서는, 이후에 None인지 검사하는 대신 False인지 검사하는 실수를 저지르기 쉽다.

  ```python
  result = careful_divide(0, 5)
  if not result:
      print('잘못된 입력')
  
  # 잘못된 입력 (result가 0이 되므로)
  
  # 출처 : [파이썬 코딩의 기술 2판] p.138
  ```

- 따라서 특별한 경우를 처리하고자 할 때, None을 반환하기보다는 예외(Exception)를 직접 발생시키는 편이 더 낫다.

  ```python
  def careful_divide(a: float, b: float) -> float:
      """a를 b로 나눈다.
      Raises:
          ValueError: b가 0이어서 나눗셈을 할 수 없을 때
      """
      try:
          return a / b
      except ZeroDivisionError as e:
          raise ValueError('잘못된 입력')
          
  # 출처 : [파이썬 코딩의 기술 2판] p.141
  ```

</hr>

## Better Way 21

> 변수 영역과 클로저의 상호작용 방식을 이해하라



#### LEGB Rule

- 식에서 **변수를 참조**할 때, 파이썬 인터프리터는 다음 순서로 영역(namespace)를 뒤진다.
  1. Local Scope (현재 함수의 영역)
  2. Enclosed Scope (현재 함수를 둘러싼 영역)
  3. Global Scope (현재 코드가 들어 있는 모듈의 영역)
  4. Built-in Scope (내장 영역)
- 식이 참조하는 이름에 해당하는 변수가 위 4가지 영역에 없으면 NameError 예외 발생

#### 클로저(closure)

- 자신이 정의된 영역 밖의 변수를 참조하는 함수
- 파이썬은 클로저를 지원한다.

#### 일급 시민 객체

- 직접 가리킬 수 있고, 변수에 대입하거나 다른 함수에 인자로 전달할 수 있으며, 식이나 if 문에서 비교하거나 함수에서 반환할 수 있는 객체
- 파이썬에서 함수는 일급 시민 객체다.



#### 변수 참조 vs 변수 대입

```python
def sort_players(players, disqualified):
    """선수들을 번호에 따라 정렬한다. 실격 선수의 경우 뒤에 따로 정렬한다.
    
    Args:
        players: 선수의 번호 목록
        disqualified: 실격 선수의 번호 목록
    """
    # dq : 실격 선수가 있으면 True, 없으면 False
    dq = False
    
    # 클로저 함수
    def check(x):
        if x in disqualified:
            dq = True
            return (1, x)
        return (0, x)
    
    players.sort(key=check)
    return dq


players = [1, 4, 7, 9, 3, 5]
disqualified = [3, 4]
print(sort_players(players, disqualified))
print(players)

# False
# [1, 5, 7, 9, 3, 4]
```

- 변수를 **참조**할 때는, LEGB Rule에 따라 현재 함수의 영역부터 내장 영역까지 차례로 변수를 찾는다.  

  =>  `check(x)` 함수는 자신을 둘러싼 영역(`Enclosed Scope`)에 있는 `disqualified` 인자에 접근 가능하다.

- 반면 변수에 값을 **대입**할 때는, 현재 함수의 영역에 변수가 정의되어 있지 않다면 상위 영역으로 탐색을 계속하지 않고, 현재 함수의 영역에서 새로운 변수를 정의한다. 

  =>  `check(x)` 함수의 `dq=True` 부분에서는, `dq` 변수가 `check(x)` 함수 내에 없으므로, `check(x)` 함수 내에 `dq`라는 새로운 변수를 정의하게 된다. 이는 `check(x)` 함수 바깥의 `dq`와는 별개의 변수이다. 따라서 sort_players 함수는 `players` 리스트에 실격 선수가 있더라도 False를 반환하게 된다.

- 그렇다면 클로저 함수에서 클로저 함수 밖의 함수 영역에 접근할 수 있는 방법은 없을까? `nonlocal` 키워드를 사용하면 가능하다. `nonlocal` 문은 말 그대로 지역변수가 아니라고 선언하는 것으로, 클로저 함수 밖(Enclosed Scope)에서 해당 변수를 탐색한다. 단, `nonlocal` 문을 사용한다고 해서 변수를 Global Scope에서까지 탐색하지는 않는다.
  - 위 코드에서 `check(x)` 함수 내에 `nonlocal dq`를 선언하면, `dq = True`는 `sort_players()` 함수의 변수 `dq`의 값을 True로 바꾸어준다.

</hr>

## Better Way 22

> 변수 위치 인자를 사용해 시각적인 잡음을 줄여라



#### *args

- `*args` 연산자를 통해 가변적인 위치 인자를 받을 수 있다.
- 빈 리스트, 빈 문자열 등 빈 시퀀스가 와도 괜찮다.

```python
def print_score(name, *scores):
    if not scores:
        print(f"{name}의 점수가 없습니다.")
    else:
        scores_str = " ".join(str(x) for x in scores)
        print(f"{name}의 점수 : {scores_str}")


print_score('가영')
print_score('나영', 70, 80, 90)

# 가영의 점수가 없습니다.
# 나영의 점수 : 70 80 90
```

- 가변 인자 함수에 시퀀스를 사용하고 싶다면, *** 연산자**를 사용하면 된다. *** 연산자**는 시퀀스의 원소들을 함수의 위치 인자로 넘기도록 한다.

```python
my_scores = [50, 100, 50]
print_score('다영', my_scores)   # 리스트 자체가 위치 인자로 들어감.
print_score('다영', *my_scores)  # 리스트의 각 원소들이 위치 인자로 들어감.

# 다영의 점수 : [50, 100, 50]
# 다영의 점수 : 50 100 50
```



가변적인 위치 인자를 받는 것에는 2가지 문제점이 있다.

1. `*args`가 받는 선택적인 위치 인자는 함수에 전달되기 전에 항상 튜플로 변환된다.

   따라서 `*args`가 받는 위치 인자의 개수가 크지 않을 때에만 사용하는 것이 좋다.

2. 함수에 새로운 위치 인자를 추가하면 해당 함수를 호출하는 모든 코드를 변경해야 한다.

   위의 `print_score()` 함수에서 갑자기 `year`라는 인자가 추가되었다고 하자. 그러면 아래와 같이 변수가 인자에 잘못 대입되는 경우가 발생할 수 있다. 이와 같은 가능성을 없애기 위해서는 `*args`를 받아들이는 함수를 확장할 때는 키워드 인자만 사용해야 한다. (=> Better Way 25)

```python
def print_score(year, name, *scores):
    if not scores:
        print(f"{name}의 점수가 없습니다.")
    else:
        scores_str = " ".join(str(x) for x in scores)
        print(f"{name}의 {year}년 점수 : {scores_str}")


print_score('나영', 70, 80, 90)

# 나영의 70년 점수 : 80 90
```

</hr>

## Better Way 23

> 키워드 인자로 선택적인 기능을 제공하라



#### 키워드 인자

- 키워드 인자를 넘기는 순서는 상관이 없다.
- 단, 위치 인자는 반드시 키워드 인자보다 앞에 있어야 한다.

```python
def book_info(title, author):
    print(f"{title} by {author}")


# 가능
book_info('어린 왕자', '생텍쥐페리')
book_info('어린 왕자', author='생텍쥐페리')
book_info(author='생텍쥐페리', title='어린 왕자')

# 불가능
book_info(title='어린 왕자', '생텍쥐페리')
# 이유 : 키워드 인자는 위치 인자보다 앞에 올 수 없다.
book_info('생텍쥐페리', title='어린 왕자')
# 이유 : 이미 '생텍쥐페리'가 title 인자에 들어간 상태에서 다시 '어린 왕자'가 title 인자에 들어갈 수는 없다.
```

- `**kwargs` 연산자는 모든 키워드 인자를 `dict`에 모아준다. 따라서 함수에서 사용하면 모든 키워드 인자를 받을 수 있다.

```python
def function_name(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")
```



키워드 인자를 사용하면 크게 3가지의 이점이 있다.

1. 어떤 파라미터를 어떤 목적에 쓰는지가 명확해진다.
2. 키워드 인자의 경우 함수 정의에서 디폴트 값을 지정할 수 있다. 
3. 기존의 호출 코드를 수정하지 않고 함수를 쉽게 확장할 수 있다.



3번에 대해서만 예시를 통해 살펴보자. 여러 카페의 정보를 관리하는 상황을 가정해보자. 처음에는 서울 내의 카페만을 대상으로 해서, 아래와 같은 함수를 작성했다.

```python
def get_cafe_info(name, revenue):
    print(f"이름: {name} | 수익: {revenue}")
    
    
get_cafe_info('스타벅스', 5000)
get_cafe_info('이디야', 3000)
# 이름: 스타벅스 | 수익: 5000
# 이름: 이디야 | 수익: 3000
```

그런데 서비스를 전국으로 확장하여, 이제 지역 정보도 추가해야 한다고 하자. 이미 정보가 입력된 카페들의 경우, 인자로 일일이 `'서울'`을 추가해야 하므로 번거롭다. 그런데 키워드 인자의 디폴트 값을 지정하면 이 문제를 해결할 수 있다.

```python
def get_cafe_info(name, revenue, location="서울"):
    print(f"지역: {location} | 이름: {name} | 수익: {revenue}")


get_cafe_info('스타벅스', 5000)
get_cafe_info('이디야', 3000)
get_cafe_info('할리스', 4000, '대전')
# 지역: 서울 | 이름: 스타벅스 | 수익: 5000
# 지역: 서울 | 이름: 이디야 | 수익: 3000
# 지역: 대전 | 이름: 할리스 | 수익: 4000
```

</hr>

## Better Way 24

> None과 독스트링을 사용해 동적인 디폴트 인자를 지정하라



- 키워드 인자의 값으로 동적으로 변하는 값을 써야 하는 경우가 있다.
- 예를 들어, 매번 메시지를 출력할 때마다 현재 시간을 함께 출력하는 경우를 생각해보자.

```python
from time import sleep
from datetime import datetime

def log(message, when=datetime.now()):
    print(f'{when}: {message}')

log('안녕!')
sleep(0.1)
log('다시 안녕!')

# 출처 : [파이썬 코딩의 기술 2판] p.157
```

- 위 코드는 원하는 대로 작동하지 않는다. 왜냐하면 **디폴트 인자의 값은 모듈이 로드될 때 단 한 번만 평가되기 때문이다.** log 함수가 정의되는 시점에 `datetime.now()`의 값이 `when` 인자에 들어간다. 그 이후로 log 함수를 쓸 때마다 처음 `when` 인자에 들어간 값이 계속 디폴트 값으로 사용되는 것이다.

- 따라서 동적인 디폴트 인자를 쓰는 경우, 디폴트 값을 None으로 지정하고, 실제 동작을 독스트링에 문서화하는 것이 일반적인 관례다.

```python
def log(message, when=None):
    """메시지와 타임스탬프를 로그에 남긴다.
    
    Args:
        message: 출력할 메시지.
        when: 메시지가 발생한 시각(datetime).
            디폴트 값은 현재 시간이다.
    """
    if when is None:
        when = datetime.now()
    
    print(f'{when}: {message}')

# 출처 : [파이썬 코딩의 기술 2판] p.158
```

- 디폴트 값에 None을 지정하는 것은 인자가 가변적인 경우에 특히 중요하다. 아래와 같은 가변 객체의 성질 때문이다.

#### 참고 -  가변 객체의 복사

`list`, `dict`, `set`과 같은 가변적인(mutable) 객체에서 `=`을 통해 복사하면, 같은 값을 가지는 새로운 객체를 생성하는 것이 아니라, 같은 주소를 가리키게 한다. 그래서 아래와 같은 일이 발생한다.

```python
list1 = [1, 3, 5, 7]
list2 = list1  # list2가 list1과 같은 객체를 가리키게 함.

list1[2] = 100
print(list1)
print(list2)

# [1, 3, 100, 7]
# [1, 3, 100, 7]
```

- 위와 같은 가변 객체의 성질로 인해, 디폴트 인자로 `[]`나 `{}` 등을 주면, 여러 값이 같은 객체를 가리키게 될 수 있다.

```python
import json

def decode(data, default={}):
    try:
        return json.loads(data)
    except ValueError:
        return default

foo = decode('잘못된 데이터')
foo['stuff'] = 5
bar = decode('또 잘못된 데이터')
bar['meep'] = 1
print('Foo:', foo)
print('Bar:', bar)

# Foo: {'stuff': 5, 'meep': 1}
# Bar: {'stuff': 5, 'meep': 1}

# 출처 : [파이썬 코딩의 기술 2판] p.159
```

- 위에서는 decode() 함수가 정의되는 순간에만 `default`값이 정의된다. 그 이후 a와 b에 각각 같은 빈 딕셔너리가 복사되고, 둘은 같은 객체를 가리키므로, 하나의 값을 변화시키면 다른 하나의 값도 변화된다.

- 위와 같은 일을 방지하기 위해서는 마찬가지로 디폴트 값을 None으로 만들고 독스트링을 쓰면 된다.

```python
def decode(data, default=None):
    """문자열로부터 JSON 데이터를 읽어온다.
    Args:
        data: 디코딩할 JSON 데이터
        default: 디코딩 실패시 반환할 값
            디폴트 값은 빈 딕셔너리
    """
    try:
        return json.loads(data)
    except ValueError:
        if default is None:
            default = {}
        return default
```

</hr>

## Better Way 25

> 위치로만 인자를 지정하게 하거나 키워드로만 인자를 지정하게 해서 함수 호출을 명확하게 만들라



#### 키워드만 사용하는 인자 (Keyword-only arguments)

- 복잡한 함수의 경우 명확성을 위해 키워드 인자를 사용하는 것이 좋다. 

- 키워드만 사용하는 인자들을 지정하고 싶은 경우, 그 인자들 앞에 `*` 기호를 넣으면 된다.

```python
def get_result(num1, num2, *, start=0, double=False):
    if double:
        return 2 * (start + num1 * num2)
    return start + num1 * num2
```

- 이제 `*` 뒤의 `start`, `double` 인자의 경우 위치 기반으로는 사용할 수 없으며, 키워드로만 사용 가능하다.

```python
print(get_result(2, 5, 10, False))
# TypeError: get_result() takes 2 positional arguments but 4 were given

print(get_result(2, 5, start=10, double=True))
# 40

print(get_result(6, 5))
# 30
```



#### 위치로만 사용하는 인자 (Positional-only arguments)

- get_result() 함수에서도 여전히 `num1`과 `num2`는 위치 인자와 키워드 인자가 혼용 가능하다.
- 위치로만 사용하는 인자들을 지정하고 싶은 경우, 그 인자들 뒤에 `/` 기호를 넣으면 된다.

```python
def get_result(num1, num2, /, *, start=0, double=False):
    if double:
        return 2 * (start + num1 * num2)
    return start + num1 * num2
```

- 이제 `/` 앞의 `num1`, `num2` 인자는 위치 기반으로만 사용할 수 있다.

```python
print(get_result(num1=6, num2=5))
# TypeError: get_result() got some positional-only arguments passed as keyword arguments: 'num1, num2'
```



- 만약 `*` 기호와 `/` 기호를 사용하면서도 위치와 키워드 둘 다로 사용 가능한 인자를 만들고 싶다면, `/`와 `*` 사이에 배치하면 된다.
- 정리하면 아래와 같다.

```bash
def func( <positional-only arguments>, `/`, <positional/keyword arguments>, `*`, <keyword-only arguments> )
```



</hr>

## Better Way 26

> `functools.wrap`을 사용해 함수 데코레이터를 정의하라



#### 데코레이터

- 자신이 감싸고 있는 함수가 호출되기 전과 후에 코드를 추가로 실행해준다.
- 자신이 감싸고 있는 함수의 입력 인자, 반환 값, 함수에서 발생한 오류에 접근할 수 있다.
- 데코레이터를 함수에 적용할 때는 `@` 기호를 사용한다.

```python
def decorator(func):
    def wrapper(*args, **kwargs):
        print('시작!')
        func(*args, **kwargs)
        print('끝!')
    return wrapper

@decorator
def printHello():
    """Hello를 출력한다."""
    print('Hello')

printHello()

# 시작!
# Hello
# 끝!
```

- 위와 같이 `@` 기호를 사용하는 것은, 함수에 대해 데코레이터를 호출한 후, 데코레이터가 반환한 결과를 원래 함수가 속해야 하는 영역에 원래 함수와 같은 이름으로 등록하는 것과 같다.

```python
printHello = decorator(printHello)
```

- 그런데 데코레이터가 반환하는 함수의 이름은 원래 함수의 이름과 달라진다. 이는 디버깅 시에 문제가 될 수 있다. 예를 들어, `help` 내장 함수를 호출하면, 함수 앞부분의 독스트링이 출력되어야 하지만, 데코레이터가 붙은 printHello 함수는 그렇지 않다.

```python
@decorator
def printHello():
    """Hello를 출력한다."""
    print('Hello')

def printPython():
    """Python을 출력한다."""
    print('Python')
    
help(printPython)
help(printHello)

""" 
Help on function printPython in module __main__:

printPython()
    Python을 출력한다.

Help on function wrapper in module __main__:

wrapper(*args, **kwargs)
"""
```



- `functools` 내장 모듈에 정의된 `wraps` 도우미 함수를 사용하면 위와 같은 문제를 해결할 수 있다. 
- `wraps`를 wrapper 함수에 적용하면, `wraps`가 데코레이터 내부에 들어가는 함수에서 중요한 메타데이터를 복사해 wrapper 함수에 적용해준다.

```python
def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        (중략)
    return wrapper

@decorator
def printHello():
    """Hello를 출력한다."""
    print('Hello')
    
help(printHello)

"""
Help on function printHello in module __main__:

printHello()
    Hello를 출력한다.
"""
```

