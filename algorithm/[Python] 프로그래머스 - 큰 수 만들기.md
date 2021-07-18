출처: 프로그래머스 코딩 테스트 연습
https://programmers.co.kr/learn/courses/30/lessons/42883
<br>

### 📃 문제 설명
<hr>

> 어떤 수에서 k개의 숫자를 제거했을 때 얻을 수 있는 가장 큰 수를 구해야 한다.

(문제 설명에는 "어떤 숫자에서 k개의 수를 제거한 가장 큰 숫자"를 구하고자 한다고 되어 있는데, 이는 `수`와 `숫자`의 개념을 혼동한 것으로 보인다.)

<br>

예를 들어, 주어진 수가 "210626"이고 k가 2라고 하면,

함수는 "210626"에서 1과 0을 제거한 "2626"을 반환해야 한다.

<br>

### 🔎 문제 접근
<hr>

`그리디 알고리즘`으로 풀 수 있다.

<br>

어떤 수에서 숫자 하나를 제거한 수를 크게 만들기 위해서는
제거한 숫자 바로 다음 숫자가 제거한 숫자보다 커야 한다. 

예를 들어, 주어진 수가 `97248`이라고 하자.

- 9는 7보다 크므로, 9를 제거하면 `7248`이 되어, 기존 수의 앞 4자리보다 작아진다.

- 7도 2보다 크므로, 7을 제거하면 `9248`이 되어, 기존 수의 앞 4자리보다 작아진다.

- 2는 4보다 작으므로, 2를 제거하면 `9748`이 되어, 기존 수의 앞 4자리보다 커진다.

- 4는 8보다 작으므로, 8을 제거하면 `9728`이 되어, 기존 수의 앞 4자리보다 커진다.

> 따라서 number에서 하나의 숫자를 제거하여 가장 큰 수를 만들기 위해서는,
> `number[i] < number[i + 1]`를 만족하는 `number[i]`를 제거해야 한다.



그리고 앞쪽의 숫자를 제거할수록 수에 더 큰 영향을 준다. 따라서`number[i] < number[i + 1]`를 만족하는 가장 작은 `i`에 대하여, `number[i]`를 제거해야 한다.

> 규칙 1 : `number[i] < number[i + 1]`를 만족하는 가장 작은 `i`에 대하여, 
> `number[i]`를 제거해야 한다.

그렇다면 `number[i] < number[i + 1]`를 만족하는 `i`가 더 이상 없는 경우는 어떻게 해야 하는가? 

이 경우에는 숫자들이 모두 내림차순 정렬되어 있으므로, 마지막 숫자를 제거하면 된다.

> 규칙 2 : `number[i] < number[i + 1]`를 만족하는 `i`가 없는 경우,
> number의 마지막 수를 제거해야 한다.

<br>

위의 규칙 1과 규칙 2를 적용하여 아래의 코드를 작성했다. 그런데 시간 초과가 떴다.


```python

def get_index_to_delete(number):
    # number[i] < number[i + 1]을 만족하는 가장 작은 i를 반환한다.
    for idx in range(len(number) - 1):
        if number[idx] < number[idx + 1]:
            return idx
    
    # number[i] < number[i + 1]을 만족하는 i가 없다면, 
    # 숫자가 내림차순 정렬되어 있다는 뜻이므로 마지막 인덱스를 반환한다.
    return len(number) - 1


def solution(number, k):
    for _ in range(k):
        i = get_index_to_delete(number)
        number = number[:i] + number[i + 1:]
    
    return number
```

<br>

### 🔑 문제 해결 과정
<hr>

##### 해결 시도 1

`number = number[:i] + number[i + 1:]` 부분에서 매번 문자열을 슬라이싱하는 것이 많은 시간을 소요하게 할 수 있다고 생각했다. 그래서 number 문자열을 리스트로 바꾸고, `del` 함수를 통해 값을 제거하는 방식으로 구현해보았다. 하지만 여전히 시간 초과가 떴다.


```python
def get_index_to_delete(number):
    # number[i] < number[i + 1]을 만족하는 가장 작은 i를 반환한다.
    for idx in range(len(number) - 1):
        if number[idx] < number[idx + 1]:
            return idx
    
    # number[i] < number[i + 1]을 만족하는 i가 없다면, 
    # 숫자가 내림차순 정렬되어 있다는 뜻이므로 마지막 인덱스를 반환한다.
    return len(number) - 1


def solution(number, k):
    num_list = list(number)
    
    for _ in range(k):
        i = get_index_to_delete(num_list)
        del num_list[i]
    
    return ''.join(num_list)
```

<br>

##### 해결 시도 2

`number[i] < number[i + 1]`를 만족하는 가장 작은 `i`를 찾을 때, 매번 문자열의 시작에서부터 탐색하는 것이 비효율적이라고 생각했다. 

만약 초기 number에서 `number[i] < number[i + 1]`가 90만 정도라고 생각해보자. 그렇다면 `number[i] < number[i + 1]`를 만족하는 `i`를 찾기 위해, 매번 90만 개 이상의 문자를 탐색해야 하는데, 이는 대단히 비효율적이다. 그래서 탐색의 시작점을 나타내는 변수 `start_index`를 추가했다.

<br>

그렇다면 `start_index`는 어떻게 정할 수 있을까? 앞선 탐색에서 `number[i] < number[i + 1]`를 만족하는 가장 작은 `i`를 구했으므로, `number[i]`를 제거하고 나면 `number[i]` 이전의 수 중에는 `number[i] < number[i + 1]`를 만족하는 수가 없다. 

다만, `number[i]`가 사라지면서 `number[i - 1]`이 `number[i] < number[i + 1]`를 만족하게 될 수는 있다. 이를테면, `98426`에서 `2`를 삭제하고 나면 `4` 뒤에 `6`이 오게 되어, 이전과 달리 `number[2] < number[3]`이 만족된다는 것이다. 

따라서 start_index는 `i - 1`로 설정하면 된다. 이번에는 시간 초과가 뜨지 않았다.

<br>

### 🔓 최종 풀이 
<hr>

```python
# number[i] < number[i + 1]을 만족하는 가장 작은 i를 반환한다.
def get_index_to_delete(number, start_idx):
    for idx in range(start_idx, len(number) - 1):
        if number[idx] < number[idx + 1]:
            return idx
            
    # number[i] < number[i + 1]을 만족하는 i가 없다면, 
    # 숫자가 내림차순 정렬되어 있다는 뜻이므로 마지막 인덱스를 반환한다.
    return len(number) - 1


def solution(number, k):
    # 탐색의 시작 인덱스 값을 저장하는 변수
    start_index = 0
    
    for _ in range(k):
        i = get_index_to_delete(number, start_index)
        number = number[:i] + number[i + 1:]
        # i가 0인 경우 예외 처리
        start_index = max(0, i - 1)
    
    return number
```