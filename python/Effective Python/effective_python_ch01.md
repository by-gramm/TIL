# 1장 파이썬답게 생각하기



## Better Way 1 

> 사용 중인 파이썬의 버전을 알아두라



#### 파이썬 버전 확인

```bash
--$ python --version
```



</hr>



## Better Way 2

> PEP 8 스타일 가이드를 따르라



#### 공백

- 탭 대신 스페이스 4칸을 사용해 들여쓰기한다.

- 긴 식을 다음 줄에 이어서 쓸 경우에는 일반적인 들여쓰기보다 4 스페이스를 더 들여써야 한다.

  ```python
  if (very_long_expression 
          another_very_long_expression):
      print()
  ```

- 함수와 클래스 사이에는 빈 줄을 두 줄 넣는다.

- 클래스 안에서 메서드와 메서드 사이에는 빈 줄을 한 줄 넣는다.

- 딕셔너리에서 키와 콜론(:) 사이에는 공백을 넣지 않고, 한 줄 안에 키와 값을 같이 넣는 경우에는 콜론 다음에 스페이스를 하나 넣는다.

- 타입  표기를 덧붙이는 경우에는 변수 이름과 콜론 사이에 공백을 넣지 않도록 주의하고, 콜론과 타입 정보 사이에는 스페이스를 하나 넣는다.

  ```python
  class Person:
      name: str
      age: int
  ```



#### 명명 규약

- 함수, 변수, 애트리뷰트 => `snake_case`
- 클래스(예외 포함) => `PascalCase`
- 보호되어야 하는 인스턴스 애트리뷰트는 _leading_underscore처럼 밑줄로 시작한다.
- private한 인스턴스 애트리뷰트는 __leading_underscore처럼 밑줄 두 개로 시작한다.
  - **private하다** = 한 클래스 내에서만 쓰이고 다른 곳에서는 쓰이지 않아야 한다

- 모듈 수준의 상수는 ALL_CAPS처럼 모든 글자를 대문자로 하고 단어와 단어 사이를 밑줄로 연결한 형태를 사용한다.

  ```python
  PI = 3.14
  ```

- 클래스에 들어 있는 **인스턴스 메서드**는 호출 대상 객체를 가리키는 첫 번째 인자의 이름으로 반드시 `self`를 사용해야 한다.

- **클래스 메서드**는 클래스를 가리키는 첫 번째 인자의 이름으로 반드시 `cls`를 사용해야 한다.

  ```python
  class Person:
      group = 'python'
      
      # 인스턴스 메서드
      def __init__(self, name):
          self.name = name
      
      # 클래스 메서드
      @classmethod
      def print_group(cls):
          print(f"소속은 {cls.group}입니다.")
  ```

  

#### 식과 문

- 컨테이너나 시퀀스가 비어 있는지를 검사할 때, 길이를 0과 비교하지 않는다. 빈 컨테이너나 시퀀스는 False로 취급되므로, `if not 컨테이너`라는 조건문을 쓴다.

  ```python
  new_list = []
  
  if not new_list:
      new_list.append(1)
  
  new_str = ""
  
  if new_str:
      new_str = ""
  ```

- 한 줄짜리 if문이나 한 줄짜리 for, while 루프, 한 줄짜리 except 복합문을 사용하지 않는다.

- 식을 한 줄 안에 다 쓸 수 없는 경우, 식을 괄호로 둘러싸고 줄바꿈과 들여쓰기를 추가해서 읽기 쉽게 만든다.

- 여러 줄에 걸쳐 식을 쓸 때는 `\` 문자보다는 괄호를 사용한다.

  ```python
  # 안 좋은 예시
  if (variable1 > variable2) and \
          (variable2 > variable3) and \
          (variable3 > variable4):
      print('')
  
  # 좋은 예시
  if ((variable1 > variable2) and
          (variable2 > variable3) and
          (variable3 > variable4) ):
      print('')
  ```



#### 임포트

- import문을 항상 파일 맨 앞에 위치시킨다.

- 모듈을 임포트할 때는 절대적인 이름(absolute name)을 사용하고, 현 모듈의 경로에 상대적인 이름은 사용하면 안 된다. 예를 들어 bar 패키지로부터 foo 모듈을 임포트한다면 `from bar import foo`라고 해야 하며, 단지 `import foo`라고 하면 안 된다.

- 반드시 상대적인 경로로 임포트해야 하는 경우에는 `from . import foo`처럼 명시적인 구문을 사용해야 한다.

- 임포트를 적을 때는 표준 라이브러리 모듈, 서드 파티 모듈, 사용자 정의 모듈 순서로 섹션을 나눠라. 각 섹션에서는 알파벳 순서로 모듈을 임포트해야 한다.

  ```python
  # 표준 라이브러리 모듈
  from math import isclose
  from math import sqrt
  # 서드 파티 모듈
  import numpy as np
  import pandas as pd
  # 사용자 정의 모듈
  import user_defined_module
  ```

  

</hr>



## Better Way 3

> bytes와 str의 차이를 알아두라



#### bytes와 str

- `bytes` 인스턴스는 이진 데이터를 저장하고, `str` 인스턴스는 유니코드 데이터를 저장한다.
  - `str` 인스턴스에는 직접 대응하는 이진 인코딩이 없다.
  - `bytes` 인스턴스에는 직접 대응하는 텍스트 인코딩이 없다.

- 따라서 `bytes` 인스턴스를 `str` 인스턴스로, 혹은 그 반대로 바꾸는 메서드가 필요하다.
  - `str`의 `encode` 메서드 : `str` 객체 => `bytes` 객체
  - `bytes`의 `decode` 메서드 : `bytes` 객체 => `str` 객체

- `bytes`와 `str` 인스턴스를 (>, ==, +, %와 같은) 연산자에 섞어서 사용할 수 없다.



#### 유니코드 샌드위치

- 파이썬 프로그램을 작성할 때 유니코드 데이터를 인코딩하거나 디코딩하는 부분을 인터페이스의 가장 먼 경계 지점에 위치시키는 방식

- 좀 더 쉽게 말하면, 최대한 빨리 디코딩하고 최대한 늦게 인코딩하는 방식
  - `bytes`로 input을 받은 후, 최대한 빨리 `str`로 변환한다.
  - 프로그램의 핵심 부분은 모두 `str`을 사용한다.
  - 핵심 부분이 끝난 후에, 다시 `bytes`로 인코딩하여 output를 내보낸다.



#### 파일 읽고 쓰기

- 이진 데이터를 파일에서 읽거나 파일에 쓰고 싶다면, 항상 이진모드(`'rb'`나 `'wb'`)로 파일을 열어야 한다.

  ```python
  # 잘못된 방식
  with open('data.bin', 'r') as f:
      data = f.read()
  # UnicodeDecodeError
  
  # 맞는 방식
  with open('data.bin', 'rb') as f:
      data = f.read()
  ```

</hr>

## Better Way 4

> C 스타일 형식 문자열을 str.format과 쓰기보다는 f-문자열을 통한 인터폴레이션을 사용하라

</hr>

## Better Way 5

> 복잡한 식을 쓰는 대신 도우미 함수를 작성하라


```python
# key가 문자열, value가 리스트인 딕셔너리에서
# key를 입력하면 해당 key값을 가지는 리스트의 첫 번째 원소를 찾고자 한다.
# 입력받은 key값 자체가 없거나, 해당 key값을 가지는 리스트가 빈 리스트라면 0을 반환한다.

num_dict = {
    '홀수': [1, 3, 5, 7, 9],
    '짝수': [2, 4, 6, 8, 10],
    '무리수': []
}

# 방법 1
first_odd_num = int(num_dict.get('홀수', [''])[0] or 0)

# 방법 2
odd_nums = num_dict.get('홀수', [''])
first_odd_num = int(odd_nums[0]) if odd_nums[0] else 0

# 방법 3
odd_nums = num_dict.get('홀수', [''])
if odd_nums[0]:
    first_odd_num = int(odd_nums[0])
else:
    first_odd_num = 0
```

위 예시에서, 아래로 갈수록 코드는 길어졌지만 가독성은 더 높아졌다. 

코드를 줄여쓰는 것보다 가독성을 좋게 하는 것이 더 가치 있다.

<br>

그리고 같은 로직을 반복할 경우, 도우미 함수를 작성해야 한다.

```python
def get_first_number(some_dict, key, default=0):
    lst = some_dict.get(key, [''])
    if lst[0]:
        return int(lst[0])
    else:
        default

        
first_odd_num = get_first_number(num_dict, '홀수')
first_even_num = get_first_number(num_dict, '짝수')
```


</hr>


## Better Way 6

> 인덱스를 사용하는 대신 대입을 사용해 데이터를 언패킹하라


## Better Way 7

> range보다는 enumerate를 사용하라


아래 코드와 같이 언패킹과 enumerate 내장 함수를 사용하면 보다 깔끔한 코드를 작성할 수 있다.



```python
# 프로그래밍 언어 점유율 1위 ~ 3위
languages = [('C', 16.21), ('Python, 12.12'), ('Java', 11.68)]

# 인덱스로 접근하는 방법
for i in range(len(languages)):
    language = languages[i]
    name = language[0]
    ratings = language[1]
    print(f'{i + 1}위: {name} (점유율: {ratings}%)')

>>>
1위: C (점유율: 16.21%)
2위: Python (점유율: 12.12%)
3위: Java (점유율: 11.68%)
    
# 언패킹과 enumerate 내장 함수를 사용하는 방법 (Better Way!)
for rank, (name, ratings) in enumerate(languages, 1):
    print(f'{rank}위: {name} (점유율: {ratings}%)')

>>>
1위: C (점유율: 16.21%)
2위: Python (점유율: 12.12%)
3위: Java (점유율: 11.68%)
```



</hr>



## Better Way 8

> 여러 이터레이터에 대해 나란히 루프를 수행하려면  zip을 사용하라



- #### 이터레이터(iterator) = 이터러블한 객체

  - 리스트, 딕셔너리, 세트, 튜플, 문자열 등



- `zip()` 함수를 통해 여러 이터레이터를 나란히 반복 순회할 수 있다.

  - `zip()` 함수는 가장 짧은 이터레이터의 순회가 끝나면 반복 순회를 종료한다.


```python
groups = ('snsd', 'shinee', 'fx', 'exo', 'red_velvet')
numbers = [1, 2, 3, 4]
agency = '에스엠'

for a, b, c in zip(groups, numbers, agency):
    print(a, b, c)

# snsd 1 에
# shinee 2 스
# fx 3 엠
```

- `itertools` 내장 모듈의 `zip_longest()` 함수는 가장 긴 이터레이터의 순회가 끝날 때까지 반복 순회한다.

  - 이미 순회가 끝난 이터레이터의 경우, `fillvalue` 속성의 값으로 대체한다.
  - `fillvalue` 속성의 디폴트값은 None이다.



```python

import itertools


a = [1, 2, 3]
b = [4, 5]

for x, y in itertools.zip_longest(a, b, fillvalue="없음"):
    print(x,y)

# 1 4
# 2 5
# 3 없음
```


</hr>


## Better Way 9

> for나 while 루프 뒤에 else 블록을 사용하지 말라



- for문이나 while문 뒤에도 else를 쓸 수 있다.
- 직관적으로는 for문이나 while문을 중간에 빠져나온 경우 else문이 실행될 것 같지만,
- 실제로는 반대로 중간에 빠져나오지 않고 반복문이 끝났을 때 else문이 실행된다.



```python

# 매개변수 num이 소수인지 판별하는 함수
def is_prime(num):
    for i in range(2, int(num ** 1 / 2) + 1):
        if num % i == 0:
            print('소수가 맞음')
    else:
        print('소수가 아님')
```

- for문이나 while문 뒤에 else문을 사용하는 구문은 반직관적이므로, 사용하지 않아야 한다.



## Better Way 10

> 대입식을 사용해 반복을 피하라



#### 대입식(assignment expression) = 왈러스 연산자(walrus operator)

- 파이썬 3.8에서 도입

- `a := b`

  - a에 b를 대입한다.
  - a의 값이 평가된다.



```python

if count:= len(students):
    print(f"학생이 {count}명입니다.")
else:
    print("학생이 없습니다.")
```

- 대입식을 사용한 위 코드는 count 변수가 if문의 첫 번째 블록에서만 의미가 있다는 점이 명확히 보이기 때문에 더 읽기 쉽다.



- 파이썬에는 switch/case문이 없다. 그래서 다중 선택처리를 해야 하는 경우, 코드가 복잡해지기 쉽다. 
- 대입식을 활용하면 switch/case문과 유사한 코드를 작성할 수 있다.

- 아래의 첫 번째 코드를 두 번째 코드로 바꿀 수 있다.

```python
if count >= 2:
    pieces = slice_bananas(count)
    to_enjoy = make_smoothies(pieces)
else:
    count = fresh_fruit.get('사과', 0)
    if count >= 4:
        to_enjoy = make_cider(count)
    else:
        count = fresh_fruit.get('레몬', 0)
        if count:
            to_enjoy = make_lemonade(count)
        else:
            to_enjoy = '아무것도 없음'

# 출처 : [파이썬 코딩의 기술 2판] p.81
```

```python
if (count := fresh_fruit.get('바나나', 0)) >= 2:
    pieces = slice_bananas(count)
    to_enjoy = make_smoothies(pieces)
elif (count := fresh_fruit.get('사과', 0)) >= 4:
    to_enjoy = make_cider(count)
elif count := fresh_fruit.get('레몬', 0):
    to_enjoy = make_lemonade(count)
else:
    to_enjoy = '아무것도 없음'
    
# 출처 : [파이썬 코딩의 기술 2판] p.82
```

