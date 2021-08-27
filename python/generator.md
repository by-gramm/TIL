# 파이썬 제너레이터

## 제너레이터의 개념

#### lazy evalution

> 계산의 결과값이 필요할 때까지 계산을 늦추는 기법 (출처 : 위키피디아)

제너레이터는 시퀀스를 생성하는 객체로, **lazy evaluation**을 따른다는 점에서 일반 함수와 다르다.

일반적인 함수는 일단 호출되면, `return`을 만날 때까지 실행된다. 그리고 `return`을 만나는 순간 함수가 끝난다. 반면 제너레이터 함수는 `yield`를 만나도 바로 함수가 끝나지 않는다. `yield`는 함수 바깥의 코드가 실행되도록 양보하여 값을 가져가게 한 뒤, 다시 제너레이터 안의 코드를 계속 실행한다.

```python
# 일반 함수
def get_square(list):
    squares = []
    for num in list:
        squares.append(num * num)
    return squares

# 제너레이터 함수
def generate_square(list):
    for num in list:
        yield num * num
```

일반 함수는 이전 호출에 대한 메모리가 없고, 항상 첫 번째 줄부터 수행된다. 반면 제너레이터는 마지막으로 호출된 항목을 기억했다가,  `next()` 메서드를 만나면 다음 `yield`에서 값을 반환한다. 순회를 마친 경우에는 `StopIteration` 에러가 발생한다.

```python
print(get_square([1, 3, 5, 7, 9]))

# [1, 9, 25, 49, 81]
```

```python
squares = generate_square([1, 3, 5, 7, 9])

print(next(squares))
# 1
print(next(squares))
# 9
print(next(squares))
# 25
print(next(squares))
# 49
print(next(squares))
# 81
print(next(squares))
# StopIteration
```

제너레이터가 생소한 이들에게도 제너레이터의 일종인 `range()` 함수는 익숙할 것이다. 

```python
for i in range(10):
    print(i)
```

위 코드에서, range(10)은 0~9의 시퀀스를 미리 만들지 않는다. 대신 for문을 돌 때마다 다음 수를 가져오고, 또 그 다음 수를 가져오는 방식으로 동작한다. 이것이 제너레이터가 동작하는 방식이다.

<br>

## 제너레이터 생성하기

#### 1. 제너레이터 함수

위에서 살펴본 것처럼 `yield`문을 사용해서 값을 반환하는 함수를 통해 제너레이터를 생성할 수 있다.

```python
def generate_square(list):
    for num in list;
        yield num * num

generator = generate_square([1, 2, 3, 4, 5])
```

#### 2. 제너레이터 컴프리헨션

리스트 컴프리헨션과 유사한 문법으로 제너레이터를 생성할 수도 있다.

```python
# 위 코드와 같은 제너레이터를 생성한다.
generator = (num * num for num in [1, 2, 3, 4, 5])
```

<br>

## 제너레이터의 특성

- 제너레이터는 메모리에 모든 입출력을 저장하지 않는다. 따라서 입력이 아주 크더라도 메모리 문제 없이 출력 시퀀스를 만들 수 있다. 1부터 100,000,000까지의 숫자로 이루어진 시퀀스를 만들어야 하는 경우를 생각해보자. 일반 함수를 활용하면, 1억개의 값을 저장한 배열을 만들어서 반환해야 하는데, 이는 메모리에 큰 부담이 될 수 있다. 반면 `range(1, 100000001)`의 제너레이터를 활용하면, 메모리에 1억개의 값을 한 번에 저장하지 않고도 1억개의 값을 순회하는 시퀀스를 만들 수 있다.

- 제너레이터는 반환할 모든 값을 미리 메모리에 저장하는 대신, 필요할 때마다 즉석에서 해당 값을 생성하고, 이터레이터를 통해 전달한다. 제너레이터는 모든 값을 기억하지 않는다. 따라서 제너레이터는 한 번만 순회할 수 있다.

```python
def get_double(list):
    for num in list:
        yield num * 2

my_generator = get_double([1, 2, 3, 4, 5])

for num in my_generator:
    print(num)

# 첫 번째 순회: 2
# 첫 번째 순회: 4
# 첫 번째 순회: 6
# 첫 번째 순회: 8
# 첫 번째 순회: 10

for num in my_generator:
    print(num)

# 이미 제너레이터가 소진되었으므로, 아무 값도 반환하지 않는다!
```

- 제너레이터를 리스트로 만들고 싶은 경우, 단순히 `list()` 함수로 감싸주면 된다.

<br>

### 참고 출처

[처음 시작하는 파이썬 2판](https://book.naver.com/bookdb/book_detail.nhn?bid=16588295)

https://ko.wikipedia.org/wiki/%EB%8A%90%EA%B8%8B%ED%95%9C_%EA%B3%84%EC%82%B0%EB%B2%95

https://www.youtube.com/watch?v=bD05uGo_sVI&ab_channel=CoreySchafer

https://dojang.io/mod/page/view.php?id=2412
