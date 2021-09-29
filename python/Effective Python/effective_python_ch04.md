# 4장 컴프리헨션과 제너레이터

<br>

## Better Way 27

> map과 filter 대신 컴프리헨션을 사용하라

#### 리스트 컴프리헨션

- 시퀀스나 이터러블에서 새 리스트를 만들어내는 간결한 구문

```python
new_str = "3 84 100 -7 -5 3"

# map과 filter를 이용한 방법
numbers = list(map(int, new_str.split()))   # [3, 84, 100, -7, -5, 3]

# 리스트 컴프리헨션을 이용한 방법
numbers = [int(x) for x in new_str.split()] # [3, 84, 100, -7, -5, 3]
```

- map과 filter를 사용하는 방식보다 보다 간결하게 리스트를 만들어낼 수 있다.
- 리스트 컴프리헨션의 다양한 사용 방법을 알고 싶다면 [이 글](https://medium.com/techtofreedom/8-levels-of-using-list-comprehension-in-python-efc3c339a1f0)을 참고하면 좋다.

```python
# 조건식 활용 가능
numbers = [int(x) for x in new_str.split() if int(x) > 0]         # [3, 84, 100, 3]
numbers = [int(x) if int(x) > 0 else 0 for x in new_str.split()]  # [3, 84, 100, 0, 0, 3]

# 원소에 변환식 지정 가능
triples = [x * 3 for x in new_str.split()]  # [9, 252, 300, -21, -15, 9]
```

- **딕셔너리 컴프리헨션**이나 **세트 컴프리헨션**도 사용 가능하다.

```python
languages = ('python', 'javascript', 'java', 'c', 'typescript')

# 딕셔너리 컴프리헨션 예시
short_languages_dict = {x: len(x) for x in languages if len(x) < 5}  # {'java': 4, 'c': 1}
```

<br>

## Better Way 28

> 컴프리헨션 내부에 제어 하위 식을 세 개 이상 사용하지 말라

- 리스트 컴프리헨션에서는 아래와 같이 **중첩 for문**을 사용할 수 있다. 

```python
board = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]

numbers = [x for r in board for x in r]  # [1, 4, 7, 2, 5, 8, 3, 6, 9]
```

- **중첩 if문**을 사용하는 것도 가능하다. if 문을 연속으로 쓰면, 이는 if 문들이 and 식으로 연결된 것과 같다.

```python
names = ['charli', 'kevin', 'thom', 'fiona', 'sam', 'kendrick']

# 길이가 5 이상이고 'jack' 보다 뒤에 있는 이름 리스트 만들기
after_jack = [name for name in names if len(name) >= 5 if name > 'jack']  # ['kevin', 'kendrick']

# 위와 같은 코드
after_jack = [name for name in names if len(name) >= 5 and if name > 'jack']
```

- 위처럼 중첩 for문이나 중첩 if문을 사용할 수 있지만, 컴프리헨션 내부에 제어식(if문, for문 등)을 3개 이상 사용하는 것은 좋지 않다. 컴프리헨션에는 최대 2개의 제어식( for문 2개 / for문 1개 + if문 1개 / if문 2개 )만 들어가는 것이 좋다. 

<br>

## Better Way 29

> 대입식을 사용해 컴프리헨션 안에서 반복 작업을 피해라

(대입식 => [Better Way 10](https://github.com/by-gramm/TIL/blob/master/python/Effective%20Python/effective_python_ch01.md#better-way-10) 참고)

- 대입식을 사용하면 컴프리헨션 안에서 반복 작업을 피할 수 있다. 
- 현재 돈으로 각 과일를 최대 몇 개씩 살 수 있는지 알아야 하는 상황을 생각해보자. 

```python
fruits = {
    'apple': 500,
    'banana': 300,
    'orange': 2000,
    'melon': 800,
}

def get_max_count(balance, price):
    """현재 잔고로 살 수 있는 과일의 개수를 구한다.
    Args:
        balance: 현재 잔고
        price: 사고자 하는 과일의 가격
    """
    return balance // price

# 1500원으로 살 수 있는 과일 목록 구하기 (대입식을 사용하지 않은 버전)
affordable_fruits = {fruit: get_max_count(1500, fruits[fruit])
                     for fruit in fruits
                     if get_max_count(1500, fruits[fruit])}

print(affordable_fruits)
# {'apple': 3, 'banana': 5, 'melon': 1}

# 대입식을 사용하면 같은 식을 더 간단하게 표현할 수 있다.
affordable_fruits = {fruit: count
                     for fruit in fruits
                     if (count := get_max_count(1500, fruits[fruit]))}
```

- 문법적으로는 값 부분에도 대입식을 사용할 수는 있지만, **조건 부분에 대입식을 사용하는 것이 좋다.**
- 값 부분에 대입식을 사용하면 오류가 발생할 수 있으며,

```python
affordable_fruits = {fruit: (count := get_max_count(1500, fruits[fruit]))
                     for fruit in fruits
                     if count}

print(affordable_fruits)

# NameError: name 'count' is not defined
# 설명 : if절은 for문과 변수 영역이 같은데, for문 내부에는 count 변수가 없으므로 오류가 발생한다.
```

- 루프 변수가 누출될 수도 있기 때문이다. 
  - 컴프리헨션이 값 부분에서 대입식을 사용할 때, 그 값에 대한 조건 부분이 없다면 루프 밖 영역으로 루프 변수가 누출된다.

```python
count = 100

affordable_fruits = {fruit: (count := get_max_count(1500, fruits[fruit]))
                     for fruit in fruits}

print(count)

# 1
# 설명 : 딕셔너리 컴프리헨션의 값 부분에서 count 변수에 대입식을 사용하고, 그 값이 조건 부분에서 사용되지 않는다. 그렇다면 이 값은 컴프리헨션 바깥으로 누출된다. 그래서 count에 마지막으로 대입되는 1이 컴프리헨션 바깥으로 누출되어, count 변수에 1이 저장되는 것이다.
```

<br>

## Better Way 30

> 리스트를 반환하기보다는 제너레이터를 사용하라

리스트를 반환하는 대신, 제너레이터를 사용하면 코드의 길이를 줄일 수 있으며, 모든 입력과 출력을 저장할 필요가 없으므로 입력이 아주 커도 출력 시퀀스를 만들 수 있다.



[직접 정리한 제너레이터 기본 개념](https://github.com/by-gramm/TIL/blob/master/python/generator.md)

<br>

## Better Way 31

> 인자에 대해 이터레이션할 때는 방어적이 돼라



이터레이터는 결과를 단 한번만 만들어낸다. 이터레이터의 일종인 제너레이터 또한 그렇다. StopIteration 예외가 발생한 제너레이터를 다시 순회하면 아무런 결과도 얻을 수 없다.

```python
def normalize(numbers):
    total = sum(numbers)    # 이터레이션이 이루어짐.
    result = []
    for value in numbers:   # 이미 모든 원소가 다 소진됨.
        percent = 100 * value / total
        result.append(percent)
    return result

# 제너레이터 함수
def read_visits(data_path):
    with open(data_path) as f:
        for line in f:
            yield int(line)
            
it = read_visits('my_numbers.txt')
percentages = normalize(it)
print(percentages)

# 출처 : [파이썬 코딩의 기술 2판] p.190 ~ 191
```

위 코드에서 `sum()` 메서드는 이터러블 객체를 인수로 받아, 이터레이션을 통해 원소들의 합을 계산한다. 이 과정에서 이미 이터러블은 다 소진된다. 이후 for문으로 같은 객체를 순회하려고 해도, 이미 원소를 다 소진했기 대문에 불가능하다.



**대안 1** : 입력 이터레이터(위 코드에서 `it`)을 명시적으로 소진시키고 이터레이터의 전체 내용을 리스트에 넣는다.

**대안 1의 문제점** : 메모리를 너무 많이 사용할 수 있다. 애초에 제너레이터를 사용하는 이유도 이 문제 때문이다.



**대안 2** : 변수가 아니라 이터레이터를 반환하는 함수를 인자로 넣는다.

```python
# get_iter는 호출될 때마다 새로운 이터레이터를 반환하는 함수
def normalize_func(get_iter):
    total = sum(get_iter())   # 새 이터레이터 생성
    result = []
    for value in get_iter():  # 새 이터레이터 생성
        percent = 100 * value / total
        result.append(percent)
    return result

path = 'my_numbers.txt'
# 람다식은 매번 제너레이터를 호출해서 새 이터레이터를 만들어낸다.
percentages = normalize_func(lambda: read_visits(path))
print(percentages)
assert sum(percentages) == 100.0

# 출처 : [파이썬 코딩의 기술 2판] p.192 ~ 193
```

**대안 2의 문제점** : 람다 함수를 인자로 넘기는 것은 보기에 좋지 않다.



**대안 3** : `이터레이터 프로토콜(iterator protocol)`을 구현한 새로운 컨테이너 클래스를 제공한다. `__iter__` 메서드를 제너레이터로 구현하면 된다.

```python
class ReadVisits:
    def __init__(self, data_path):
        self.data_path = data_path

    def __iter__(self):
        with open(self.data_path) as f:
            for line in f:
                yield int(line)

visits = ReadVisits(path)
percentages = normalize(visits)
print(percentages)
assert sum(percentages) == 100.0

# 출처 : [파이썬 코딩의 기술 2판] p.193 ~ 194
```

<br>

## Better Way 32

> 긴 리스트 컴프리헨션보다는 제너레이터 식을 사용하라

#### 제너레이터 컴프리헨션

- 리스트 컴프리헨션과 유사한 방식으로 제너레이터를 생성할 수 있다.

```python
numbers = [1, 2, 3, 4, 5]
generator = (num * num for num in numbers)
```

- 두 제너레이터 식을 합성할 수도 있다.

```python
joined_generator = (num * 3 for num in generator)

for num in joined_generator:
    print(num)

# 3
# 12
# 27
# 48
# 75
```

<br>

## Better Way 33

> yield from을 사용해 여러 제너레이터를 합성하라

여러 제너레이터를 합성할 때 `yield from` 식을 사용하면, 코드의 가독성도 높아지며 성능도 좋아진다.

```python
def generator1():
    for i in range(1, 100, 2):
        yield i

def generator2():
    for j in range(2, 100, 2):
        yield j

def generator():
    yield from generator1()  
    yield from generator2()
```

<br>

## Better Way 34

> send로 제너레이터에 데이터를 주입하지 말라

(내용 추가 예정)

<br>

## Better Way 35

> 제너레이터 안에서 throw로 상태를 변화시키지 말라

(내용 추가 예정)

<br>

## Better Way 36

> 이터레이터나 제너레이터를 다룰 때는 itertools를 사용하라

[itertools 공식 문서](https://docs.python.org/3/library/itertools.html)



#### 여러 이터레이터 연결하기

`chain`

- 여러 이터레이터를 하나의 순차적인 이터레이터로 합친다.

`repeat`

- 하나의 값을 반복해서 내놓는다. 두 번째 인수로 최대 횟수를 지정하면, 이터레이터가 값을 내놓는 횟수를 제한할 수 있다.

`cycle`

- 이터레이터의 원소들을 반복해서 내놓는다.

`tee`

- 한 이터레이터를 두 번째 인자로 지정된 개수만큼의 이터레이터로 만든다.

`zip_longest`

- zip 함수와 같은 방식으로 작동하지만, 가장 긴 이터레이터를 기준으로 순회를 종료한다. 짧은 쪽 이터레이터의 원소를 다 사용한 경우 `fillvalue`로 지정한 값을 채워 넣어준다.

- `fillvalue`의 기본값은 None이다.

```python
import itertools

it = itertools.cycle([1, 2])
result = [next(it) for _ in range (10)]
print(result)

# [1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
```

```python
keys = ['하나', '둘', '셋']
values = [1, 2]

normal = list(zip(keys, values))
print('zip:', normal)

it = itertools.zip_longest(keys, values, fillvalue='없음')
longest = list(it)
print('zip_longest:', longest)

# zip: [('하나', 1), ('둘', 2)]
# zip_longest: [('하나', 1), ('둘', 2), ('셋', '없음')]
```

<br>

#### 이터레이터에서 원소 거르기

`islice`

- 시퀀스 슬라이싱과 비슷하게 작동한다.

- 끝만 지정하거나, 시작과 끝을 지정하거나, 시작과 끝과 증가값을 지정할 수 있다.

`takewhile`

- 술어가 False를 반환하는 첫 원소가 나타나기 전까지 원소를 돌려준다.

`dropwhile`

- `takewhile`의 반대다. 술어가 True를 반환하는 동안 원소를 건너뛴다.

`filterfalse`

- `filter`의 반대다. 주어진 이터레이터에서 술어가 False를 반환하는 모든 원소를 리턴한다.

```python
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
less_than_seven = lambda x: x < 7

it = itertools.takewhile(less_than_seven, values)
print(list(it))

# [1, 2, 3, 4, 5, 6]

it = itertools.dropwhile(less_than_seven, values)
print(list(it))

# [7, 8, 9, 10]
```

<br>

#### 이터레이터에서 원소의 조합 만들어내기

`accumulate`

- 두 번째 인수로 받는 이항 함수를 반복 적용하면서 원소를 값 하나로 줄여준다. (**누적된 값**을 저장한다.)

- 이항 함수를 넘기지 않으면 주어진 입력 이터레이터 원소의 합계를 계산한다.

`product`

- 이터레이터에 들어 있는 아이템들의 **데카르트 곱(Cartesian product)**을 반환한다.

`permutations`

- 이터레이터가 내놓는 원소들로부터 만들어낸 길이 n의 **순열**을 리턴한다.

`combinations`

- 이터레이터가 내놓는 원소들로부터 만들어낸 길이 n의 **조합**을 리턴한다.

`combinations_with_replacement`

- 이터레이터가 내놓는 원소들로부터 만들어낸 길이 n의 **중복 조합**을 리턴한다.

```python
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
sum_reduce = itertools.accumulate(values)
print('누적 합:', list(sum_reduce))

# 누적 합: [1, 3, 6, 10, 15, 21, 28, 36, 45, 55]

p = itertools.permutations([1, 2, 3], 2)
print('순열:', list(p))

# 순열: [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]

c = itertools.combinations([1, 2, 3], 2)
print('조합:', list(c))

# 조합: [(1, 2), (1, 3), (2, 3)]

c2 = itertools.combinations_with_replacement([1, 2, 3], 2)
print('중복 조합:', list(c2))

# 중복 조합: [(1, 1), (1, 2), (1, 3), (2, 2), (2, 3)]
```

