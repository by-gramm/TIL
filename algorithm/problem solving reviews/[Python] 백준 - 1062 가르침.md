출처: 백준 온라인 저지
https://www.acmicpc.net/problem/1062

<br>

___

### 📃 문제 설명

anta로 시작해서 tica로 끝나는 n개의 단어가 주어진다. 

ex. `antadeftica` / `antapythontica` / `antahomeruntica` 등

k개의 알파벳을 통해 표현할 수 있는 단어의 최대 개수를 구해야 한다.

<br>

모든 단어가 anta로 시작해서 tica로 끝나므로, `a / c / i / n / t`는 반드시 포함되어야 한다. 따라서 k가 5보다 작다면 표현 가능한 단어의 개수는 0개다. 

k가 5 이상이라면, 각 단어에서 `a / c / i / n / t` 이외의 부분들을 `k - 5`개의 알파벳으로 표현할 수 있는 개수를 구해야 한다.

<br>


### ⏰ 시간 초과 풀이

가장 먼저 생각할 수 있는 방법은 `a / c / i / n / t` 이외의 알파벳 중 `k - 5`개의 알파벳을 고르는 모든 경우에 표현 가능한 단어의 개수를 구하는 것이다. 아래 코드와 같이 구현했으며, 예상대로 시간 초과가 떴다. 

```python

from sys import stdin
from itertools import combinations
from string import ascii_lowercase


n, k = map(int, stdin.readline().split())
words = []
# 각 입력 단어에 대하여
# 1. 앞의 anta와 뒤의 tica를 슬라이스한 뒤 set로 만들고
# 2. 그중 a/c/i/t/n을 제외한 뒤 words 리스트에 저장
for _ in range(n):
    words.append(set(stdin.readline().rstrip()[4:-4]).difference('a', 'c', 'i', 't', 'n'))

# a/c/i/t/n을 제외한 알파벳 모음
except_acitn = set(ascii_lowercase).difference('a', 'c', 'i', 't', 'n')
max_count = 0

if k < 5:
    print(0)

else:
    # a/c/i/t/n과 a/c/i/t/n을 제외한 알파벳 중 k - 5개를 고른 조합으로
    # 만들 수 있는 단어 개수의 최대값을 구한다.
    for x in list(combinations(except_acitn, k - 5)):
        count = 0
        for word in words:
            if not word.difference(x):
                count += 1

        max_count = max(max_count, count)

    print(max_count)
```


<br>

### 🔑 문제 해결 과정

검색해보니, `비트마스크(bit mask)`를 통해 이 문제를 해결할 수 있다는 점을 알게 되었다. 비트마스크는 비트 연산을 이용한 문제 해결 기술이다. 비트 연산으로 이 문제를 어떻게 해결할 수 있을지 생각해 보았다.

<br>

내가 생각한 방법은 다음과 같다.

1. 우선 처음 했던 것과 같이, 각 단어들에서 `a / c / i / n / t`을 제외한 알파벳의 set를 구한다. 예를 들어, 단어가 `antabxbtica`라면, 이를 {'b', 'x'}로 만든다.

2. `a / c / i / n / t`을 제외한 알파벳을 키로 가지고, 각각 0부터 20까지의 수를 값으로 가지는 딕셔너리 `bin_dict`를 만든다. b가 20, d가 19 ... z가 0이다.

3. `a / c / i / n / t`을 제외한 알파벳 배열을 2진수 숫자로 만들어주는 함수 `word_to_bin`을 만든다. 예를 들어, 함수의 입력값이 `bbfxz`라면, 출력값은 `0b100100000000000000101`이다. ('b', 'f', 'x', 'z'가 각각 21개 알파벳 중 1 / 4 / 19 / 21번째이므로, 1 / 4 / 19 / 21번째 숫자만 1이다.) 물론 이 함수에 값을 넣기 전에는 미리 `a / c / i / n / t`을 없애주어야 한다.

4. k가 5보다 작다면, 만들 수 있는 단어의 최대 개수는 0이다.

5. k가 5 이상이라면, `a / c / i / n / t`을 제외한 21개의 알파벳 중 `k - 5`개의 알파벳으로 만들 수 있는 모든 조합에 대하여, 표현할 수 있는 단어의 개수를 구한다. 그 값의 최대값이 정답이 될 것이다. `k - 5`개의 알파벳의 조합은 2진수로 표현한다. 예를 들어, ('b', 'd', 'z')라면, `0b101000000000000000001`로 표현한다. ('b', 'd', 'z'가 각각 21개 알파벳 중 1 / 3 / 21번째이므로, 1 / 3 / 21번째 숫자만 1이다.)

<br>

문제는 `k - 5`개의 알파벳으로 만들 수 있는 모든 조합을 구하는 방법이었다. 

21개 중 `k - 5`개로 만드는 조합은 `itertools.combinations` 함수로 구할 수 있다. 하지만 이번 경우는 n개의 조합이 아니라, 1이 n개 들어간 2진수를 구해야 하므로, 같은 방법을 사용할 수는 없다.

그래서 아예 모든 경우의 10진수 값을 구한 뒤, 이를 2진수로 바꾸어 주기로 했다.

<br>

21자리 중 1이 n개 들어간 2진수는 2의 0제곱 ~ 2의 20제곱 중 n개의 합을 2진수로 바꾼 값과 같다. 예를 들어, `0b10101`은 `2^4 + 2^2 + 2^0`을 2진수로 바꾼 값이다. 

그래서 2의 0제곱부터 2의 20제곱까지 저장한 리스트를 만든 뒤, `itertools.combinations`를 통해 이중 `k - 5`개를 뽑는 모든 조합을 구하도록 했다. 

이 조합 각각에 대하여, 조합의 모든 수의 합을 구해 2진수로 바꾸어주면, 결과적으로 21자리 중 1이 `k - 5`개 들어간 모든 2진수를 구할 수 있다.

<br>

### 🔓 정답 풀이

```python

from sys import stdin
from itertools import combinations


# bin_dict : a/c/i/t/n을 제외한 알파벳 각각에 임의의 고유 번호를 부여한 딕셔너리
bin_dict = {'b': 20, 'd': 19, 'e': 18, 'f': 17, 'g': 16, 'h': 15, 'j': 14,
            'k': 13, 'l': 12, 'm': 11, 'o': 10, 'p': 9, 'q': 8, 'r': 7,
            's': 6, 'u': 5, 'v': 4, 'w': 3, 'x': 2, 'y': 1, 'z': 0}


# 알파벳 배열을 2진수로 바꾸어주는 함수
def word_to_bin(word):
    answer = 0b0
    for x in word:
        answer = answer | (1 << bin_dict[x])

    return answer


n, k = map(int, stdin.readline().split())
words = []
# 각 입력 단어에 대하여
# 1. 앞의 anta와 뒤의 tica를 슬라이스한 뒤 set로 만들고
# 2. 그중 a/c/i/t/n을 제외한 뒤 words 리스트에 저장
for _ in range(n):
    words.append(set(stdin.readline().rstrip()[4:-4]).difference('a', 'c', 'i', 't', 'n'))

# k가 5 미만이라면 어떤 단어도 만들 수 없음.
if k < 5:
    print(0)
else:
    bin_list = [word_to_bin(x) for x in words]
    max_count = 0

    # 2의 0제곱부터 2의 20제곱까지 저장한 리스트
    power_of_2 = [2 ** i for i in range(21)]

    # 현재 순회 중인 k - 5개의 알파벳 조합(comb)으로
    for comb in combinations(power_of_2, k - 5):
        current = sum(comb)
        count = 0
        for bin_number in bin_list:
            # 현재 순회 중인 단어를 만들 수 있다면
            if bin_number & current == bin_number:
                # count에 1을 더한다.
                count += 1

        # count = comb로 만들 수 있는 단어의 개수
        max_count = max(max_count, count)

    print(max_count)

```