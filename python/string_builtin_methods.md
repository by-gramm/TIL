# [Python] 문자열 관련 메서드

며칠 후 보는 네이버 코딩테스트에서는 외부 IDE 사용이나 검색이 불가능하다. 그래서 메서드 사용법을 잘 익혀두지 않으면, 문법 자체를 생각하느라 시간을 많이 소요할 수도 있다. 그런 일을 방지하기 위해, 파이썬 내장 메서드 중 가장 헷갈리는 문자열 관련 메서드들을 정리해보았다. (문자열 메서드 이외에 내장 함수인 `chr()`, `ord()`와 string 모듈도 함께 정리해보았다.)

<br>



### 검사

##### str.isalnum()

> 문자와 숫자로만 이루어졌는지 확인한다.



##### str.isalpha()

> 문자로만 이루어졌는지 확인한다.



##### str.isdigit()

> 숫자로만 이루어졌는지 확인한다.



##### str.islower()

> 소문자로만 이루어졌는지 확인한다.



##### str.isupper()

> 대문자로만 이루어졌는지 확인한다.
>
> 

##### str1.startswith(str2)

> str1이 str2로 시작하는지 확인한다.
>
> 두번째 인자로 n을 넣으면 n번째 문자부터 검사할 수 있다.



##### str1.endswith(str2)

> str1이 str2로 끝나는지 확인한다. 

<br>

### 탐색

##### str.find(x, start, end)

> str의 start ~ end 범위 내에서 x의 첫번째 인덱스를 반환한다. (x가 없으면 -1 반환)
>
> find(x) / find(x, start) / find(x, start, end) 모두 가능



##### str.rfind(x, start, end)

> str의 start ~ end 범위 내에서 x의 마지막 인덱스를 반환한다. (x가 없으면 -1 반환)
>
> rfind(x) / rfind(x, start) / rfind(x, start, end) 모두 가능

<br>

### 정렬 / 공백 처리

##### str.ljust(n)

> n자리 내에서 왼쪽 정렬한다.

```python
'abc'.ljust(6)  # "   abc"
```



##### str.rjust(n)

> n자리 내에서 오른쪽 정렬한다.



##### str.center(n)

> n자리 내에서 가운데 정렬한다.



##### str.zfill(n)

> n자리가 되도록 문자열 앞에 0을 채워준다.
>
> str의 자리수가 n보다 큰 경우에는 아무런 변화가 없다.



##### str.strip([chars])

> 문자열의 양쪽 끝에서 공백 문자를 제거한 문자열의 복사본을 반환한다. (단, 원본 문자열은 그대로다.)
>
> [chars]에 문자 집합을 넣으면, 양쪽에서 해당 문자들을 모두 제거한다.

```python
new_str = "          alone     "

new_str.strip()  # "alone"
new_str          # "          alone     "
```

```python
lyrics = "aespa is me there can't be two"

lyrics.strip('aeiou')  # "spa is me there can't be tw"
```



##### str.lstrip([chars])

> 문자열의 왼쪽에서 공백 문자 / 주어진 문자 집합을 제거한 문자열의 복사본을 반환한다.



##### str.rstrip([chars])

> 문자열의 오른쪽에서 공백 문자 / 주어진 문자 집합을 제거한 문자열의 복사본을 반환한다.

<br>

### 대소문자 변환

##### str.upper()

> 문자열의 모든 문자를 대문자로 바꾸어준다.



##### str.lower()

> 문자열의 모든 문자를 소문자로 바꾸어준다.



##### str.title()

> 각 단어의 앞 문자를 대문자로, 나머지 문자를 소문자로 바꾸어준다.



##### str.capitalize()

> 전체 문자열의 첫 문자만 대문자로, 나머지 문자를 소문자로 바꾸어준다.

```python
name = 'my bloody valentiNE'

name.title()       # My Bloody Valentine
name.capitalize()  # My bloody valentine
```



##### str.swapcase()

> 문자열의 소문자는 대문자로, 대문자는 소문자로 바꾸어준다.

<br>

### 형식 변환

##### chr()

> 문자를 아스키코드 수로 변환한다.

```python
# 아스키코드에서 아래 2개 정도는 외워두면 좋다.

chr(65)  # 'A'
chr(97)  # 'a'
```



##### ord()

> 아스키코드 수를 문자로 변환한다.



##### sep.join(iterable)

> iterable의 문자열들을 sep(구분자)로 구분하여 이어붙인 문자열을 반환한다.



##### str.split(sep)

> str을 sep(구분자)를 기준으로 나누어 리스트로 변환한다.

```python
', '.join(['one', 'two', 'three'])
# one, two, three

'DJ Shadow - Endtroducing...'.split(' ')
# ['DJ', 'shadow', '-', 'Endtroducing...']
```



##### str.partition(sep)

> str을 sep(구분자)이 처음 나타나는 위치를 기준으로 구분한다. (구분자도 리스트에 포함된다.)

```python
email_address = 'python@gmail.com'

email_address.partition('@')  # ['python, '@', 'gmail.com']
```

<br>

### 그 외

##### str.count(x, start, end)

> str의 start ~ end 범위에서 문자열 x의 개수를 반환한다.
>
> count(x) / count(x, start) / count(x, start, end) 모두 가능



##### str.replace(old, new)

> str에 있는 문자열 old를 모두 문자열 new로 바꾼 새 문자열을 반환한다. (원본 문자열은 변화 X)
>
> 세번째 인자 count를 넣으면, count의 개수만큼만 문자열을 바꿔준다.

```python
lyrics = "Naevis, 우리 ae, ae들을 불러봐"

lyrics.replace('ae', '@')    # N@vis, 우리 @, @들을 불러봐
lyrics.replace('ae', '', 1)  # Nvis, 우리 ae, ae들을 불러봐
```

```python
# 주로 아래와 같이 문자열에서 특정 문자나 공백을 제거하기 위해 사용한다.

new_str = "django rest framework"

new_str.replace('a', '').replace('e', '')  # djngo rst frmwork
new_str.replace(" ", "")  # djangorestframework
```



##### 추가) string 모듈

```python
import string
 
    
string.ascii_letters    # abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
string.ascii_lowercase  # abcdefghijklmnopqrstuvwxyz
string.ascii_uppercase  # ABCDEFGHIJKLMNOPQRSTUVWXYZ
string.digits           # 0123456789
```



