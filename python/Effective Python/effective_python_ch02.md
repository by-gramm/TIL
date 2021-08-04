# 2장 리스트와 딕셔너리


## Better Way 11

> 시퀀스를 슬라이싱하는 방법을 익혀라



- 슬라이싱할 때 시퀀스의 범위를 넘어가는 인덱스는 무시된다.

  ```python
  fruits = ['apple', 'banana', 'melon']
  print(fruits[:20])
  
  # ['apple', 'banana', 'melon']
  ```

- 리스트를 새로운 식별자에 대입하면, 같은 주소를 참조한다. 따라서 한 리스트의 값을 변화시키면, 같은 주소를 참조하고 있는 다른 리스트의 값도 변경된다.

- 반면 리스트를 슬라이싱하면 새로운 리스트가 생성된다. 이 새로운 리스트는 다른 주소를 가지고 있으므로, 한 리스트의 값을 변화시켜도 다른 리스트의 값은 바뀌지 않는다.

  ```python
  a = [1, 3, 5, 7, 9]
  b = a
  b[3] = 100
  print(b)
  print(a)
  
  # [1, 3, 5, 100, 9]
  # [1, 3, 5, 100, 9]
  ```
  
  ```python
  a = [1, 3, 5, 7, 9]
  c = a[:]
  c[3] = 100
  print(c)
  print(a)
  
  # [1, 3, 5, 100, 9]
  # [1, 3, 5, 7, 9]
  ```

</hr>

## Better Way 12

> 스트라이드(step)와 슬라이스를 한 식에 함께 사용하지 말라



- 슬라이싱을 할 때, 시작값 / 끝값 / 증가값이 모두 있으면 혼란스럽기 때문에 함께 사용하지 않는 것이 좋다. 

  (개인적으로는 `a[1::2]` 정도는 괜찮을 것 같지만, 음수 인덱스를 사용한 경우에는 증가값을 사용하지 않는 것이 좋을 것 같다.)

</hr>

## Better Way 13

> 슬라이싱보다는 나머지를 모두 잡아내는 언패킹을 사용하라



#### 별표 식(starred expression)

- 별표 식은 언패킹 패턴의 다른 부분에 들어가지 못하는 모든 값을 담는다.

- 별표 식은 항상 `list` 인스턴스가 된다.

- 별표 식은 언패킹 패턴의 어떤 위치에도 놓을 수 있다.

  ```python
  archery_ranks = ['korea', 'netherlands', 'mexico', 'turkey', 'france']
  gold_medal, silver_medal, *others = archery_ranks
  
  print(gold_medal, silver_medal, others)
  
  # 출력 결과: korea netherlands ['mexico', 'turkey', 'france']
  ```

  ```python
  numbers = [1, 3, 5, 7, 9]
  smallest, *others, biggest = numbers
  
  print(smallest, others, biggest)
  
  # 출력 결과: 1 [3, 5, 7] 9
  ```

- 주의 1) 별표 식만 사용해서 언패킹할 수는 없다. 별표 식만으로 언패킹할 경우 `SyntaxError`가 발생한다.

  ```python
  archery_ranks = ['korea', 'netherlands', 'mexico', 'turkey', 'france']
  *others = archery_ranks
  
  # SyntaxError: starred assignment target must be in a list or tuple
  ```

- 주의 2) 한 수준의 언패킹 패턴에 별표 식을 2개 이상 쓸 수는 없다. 상식적으로 생각해보면, 별표식이 여러 개라면 어디까지 포함시켜야할지 알 수 없으므로 당연한 규칙이다.

  ```python
  archery_ranks = ['korea', 'netherlands', 'mexico', 'turkey', 'france']
  first, *great, *good = archery_ranks
  
  # SyntaxError: multiple starred expressions in assignment
  ```

</hr>

## Better Way 14

> 복잡한 기준을 사용해 정렬할 때는 key 파라미터를 사용하라



- 리스트를 정렬하는 `sort` 메서드에서 `key` 파라미터를 사용하면, 원하는 기준을 사용하여 정렬할 수 있다. `key` 파라미터에는 함수가 들어가야 하는데, 주로 여기에서 람다식을 사용한다.

  ```python
  class Player:
      def __init__(self, name, age):
          self.name = name
          self.age = age
  
          
  players = [
      Player('An San', 21),
      Player('Jedeok Kim', 18),
      Player('Yubin Shin', 18),
      Player('Yeongyeong Kim', 34)
  ]
  
  # 이름순으로 정렬
  players.sort(key=lambda x: x.name)
  # 나이순으로 정렬
  players.sort(key=lambda x: x.age)
  ```

- `key` 함수를 이용해 원소 값을 변형한 뒤, 그 값을 기준으로 정렬하는 것도 가능하다.

  ```python
  numbers = [1, 5, -7, 9, -3]
  numbers.sort(key=lambda x: abs(x))
  
  print(numbers)
  # [1, -3, 5, -7, 9]
  ```

- `key` 파라미터를 이용하는 방식은 특히 **여러 기준을 사용해 정렬할 때** 유용하게 사용될 수 있다.



####  여러 기준을 사용해 정렬하기

- 정렬에 사용할 속성들을 우선순위에 따라 튜플에 넣어 반환하는 람다식을 사용한다.

  ```python
  # 나이순으로 정렬한 뒤, 이름순으로 정렬
  players.sort(key=lambda x: (x.age, x.name))	
  ```

- 다만 이렇게 할 경우, `reverse` 파라미터를 한 번만 쓸 수 있으므로, 정렬 방향이 모두 오름차순이거나 모두 내림차순이어야 한다. 그렇다면 나이순으로 오름차순 정렬한 뒤, 이름순으로 내림차순 정렬할 수는 없을까? 숫자 값의 경우, 단항 부호 반전 연산자(`-`)를 사용하면 가능하다.

  ```python
  # 나이순으로 오름차순 정렬한 뒤, 이름순으로 내림차순 정렬
  players.sort(key=lambda x: (-x.age, x.name), reverse=True)
  ```

- 하지만 문자열과 같은 타입의 경우 단항 부호 반전 연산자를 사용할 수 없다. 이 경우, `sort` 메서드를 여러번 사용하면 된다. `sort` 메서드는 기존 순서를 유지하는 방식으로 정렬을 수행하기 때문이다. 예를 들어 나이순으로 정렬한 뒤, 이름순으로 정렬하면, 이름이 같은 값들끼리는 나이순 정렬이 유지된다는 것이다. 이때 주의해야 할 점은, **정렬 기준 우선순위의 역순으로 정렬을 수행해야 한다**는 점이다.

  ```python
  # A와 B는 모두 1) 나이순으로 내림차순 정렬, 2) 이름순으로 내림차순 정렬한다.
  
  # A
  players.sort(key=lambda x: (x.age, x.name), reverse=True)
  
  # B
  players.sort(key=lambda x: x.name, reverse=True)
  players.sort(key=lambda x: x.age, reverse=True)
  ```

</hr>

## Better Way 15

> 딕셔너리 삽입 순서에 의존할 때는 조심하라



- 파이썬 3.5까지는 딕셔너리가 삽입 순서를 보장하지 않았다.
- 파이썬 3.6부터는 딕셔너리가 삽입 순서를 보장한다.
- 하지만 파이썬은 **덕 타이핑**에 의존하므로, 삽입 순서가 보장된다고 가정하지 않는 것이 좋다.



#### 덕 타이핑(duck typing)

> **Duck typing** in computer programming is an application of the duck test — "If it walks like a duck and it quacks like a duck, then it must be a duck"—to determine whether an object can be used for a particular purpose. With normal typing, suitability is determined by an object's type. In duck typing, an object's suitability is determined by the presence of certain methods and properties, rather than the type of the object itself. 
>
> (출처 : https://en.wikipedia.org/wiki/Duck_typing)

- 객체의 타입 자체를 엄밀하게 따지는 대신, 실행 시점의 속성과 메서드에 따라 판단하는 방식이다. 

- 이를테면, 딕셔너리의 프로토콜을 지키지만, 삽입 순서를 보장하지 않는 클래스가 있을 수 있다. 이 경우, 파이썬은 덕 타이핑에 의존하므로, 딕셔너리가 들어갈 자리에 이 새로운 클래스가 자리할 수 있다. 그래서 딕셔너리의 삽입 순서 보장을 믿고 코드를 짰지만 예상과 다른 결과가 나올 수 있다.

- 딕셔너리와 같은 자료형을 조심스럽게 다루는 방법은 아래 3가지가 있다.

  1. `dict` 인스턴스의 삽입 순서 보존에 의존하지 않는 방법
  2. 실행 시점에 명시적으로 `dict` 타입을 검사하는 방법

  ```python
  # ranks 객체가 dict 타입이 아니라면
  if not isinstance(ranks, dict):
      raise TypeError('dict 인스턴스가 아닙니다.')
  ```

  3. 타입 애너테이션과 정적 분석을 사용해 `dict` 값을 요구하는 방법

  ```python
  def get_winner(ranks: Dict[str, int]) -> str:
      return next(iter(ranks))
  ```

</hr>

## Better Way 16

> in을 사용하고 딕셔너리 키가 없을 때 KeyError를 처리하기보다는 get을 사용하라



#### 딕셔너리 키가 없는 경우를 처리하는 방법

1. ﻿`in` 식을 사용하는 방법

   ```python
   if key in votes:
       names = votes[key]
   # key가 votes 딕셔너리에 없으면
   else:
       votes[key] = names = []
   ```

2. `KeyError` 예외를 사용하는 방법

   ```python
   try:
       names = votes[key]
   # key가 votes 딕셔너리에 없으면 KeyError 발생
   except KeyError:
       votes[key] = names = []
   ```

3. `get` 메서드를 사용하는 방법

   ```python
   names = votes.get(key, "")
   # get 함수는 key값이 딕셔너리에 없는 경우 default값 반환
   if not names:
       votes[key] = names = []
   ```

4. `setdefault` 메서드를 사용하는 방법

   ```python
   names = votes.setdefault(key, [])
   ```

- `dict.setdefault(keyname, value)`
  - `keyname` (필수) : 탐색하는 key값
  - `value` (선택) : `keyname`이 딕셔너리에 없는 경우, 이 값이 key의 값이 됨. 디폴트는 None

5. `dict`의 하위 클래스와 `__missing__` 메서드를 사용하는 방법 (=> Better Way 18)



- ﻿1, 2번보다는 `get` 메서드를 사용하는 3번이 코드가 훨씬 간결하다. 

- 4번은 코드가 더 짧긴 하지만, 가독성은 떨어진다. 

- 가급적이면 `get` 메서드를 사용하는 것이 좋다. 

- `setdefault` 메서드를 사용하는 것이 적합해 보일 때는 `defaultdict`를 고려해보자. (Better Way 17)

</hr>

## Better Way 17

> 내부 상태에서 원소가 없는 경우를 처리할 때는 setdefault보다 defaultdict를 사용하라



#### defaultdict 메서드

- `collections.defaultdict(default_factory, key=value...)`
  - `default_factory` : 디폴트 값을 반환하는 함수

- `key`값이 없는 경우 `default_factory`가 반환하는 디폴트 값을 반환하는 딕셔너리다.

  ```python
  from collections import defaultdict
  
  
  ex1 = defaultdict(int, a=5, b=8)
  print(ex1['a'])
  print(ex1['c'])
  
  # 5
  # 0
  
  ex2 = defaultdict(list, a=[5, 6], b=[7, 8])
  print(ex2['a'])
  print(ex2['c'])
  
  # [5, 6]
  # []
  ```

</hr>

## Better Way 18

> `__missing__`을 사용해 키에 따라 다른 디폴트 값을 생성하는 방법을 알아두라



- 딕셔너리에 존재하지 않는 키에 접근하면 `KeyError`가 발생한다.

```python
gold_medals = {
    'china': 32,
    'america': 25,
    'japan': 21,
    'uk': 15,
    'australia': 15
}

print(gold_medals['france'])

# KeyError: 'france'
```

- 이를 방지하기 위해서, 딕셔너리 클래스를 상속 받은 하위 클래스에 `__missing__` 메서드를 정의하면, 주어진 키 값이 없는 경우를 처리할 수 있다.

```python
# dict의 하위 클래스와 __missing__ 메서드 정의
class Subdict(dict):
    def __missing__(self, country):
        return f'{country}의 금메달 정보는 없습니다.'
    

gold_medals = Subdict({
    'china': 32,
    'america': 25,
    'japan': 21,
    'uk': 15,
    'australia': 15
})

print(gold_medals['france'])

# france의 금메달 정보는 없습니다.
```

- `defaultdict`에 전달되는 함수는 인자를 받지 않아서, 접근에 사용한 **키 값에 맞는 디폴트 값**을 생성하는 것은 불가능하다. 만약 키 값에 맞는 디폴트 값을 생성해야 하는 경우, 위와 같이 직접 `dict`의 하위 클래스와 `__missing__` 메서드를 정의하면 된다.

