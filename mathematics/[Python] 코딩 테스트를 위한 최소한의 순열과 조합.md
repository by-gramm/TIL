### 순열과 조합의 개념

- **순열(permutation)**

 n개 중 r개를 선택한 뒤, 순서대로 정렬하는 것

- **조합(combination)**

 n개 중 r개를 선택하는 것 (순열과 달리 순서는 고려하지 않음.)

- (A, B, C)로 만든 길이 2의 순열 : (A, B) (A, C) (B, A) (B, C) (C, A) (C, B)

- (A, B, C)로 만든 길이 2의 조합 : (A, B) (A, C) (B, C)

<br>

### 순열/조합 공식

- **순열** : n개 중 r개를 뽑아서 정렬하는 경우의 수

  $$_nP_r = {n! \over (n - r)!}$$
  
- **조합** : n개 중 r개를 뽑는 경우의 수

  $$_nC_r = {n! \over (n - r)!r!}$$
  
- **중복 순열** : n개 중 r개를 `중복을 허용해서` 뽑아서 정렬하는 경우의 수

  $$n^r$$
  
- **중복 조합** : n개 중 r개를 `중복을 허용해서` 뽑는 경우의 수

  $$_{n+r-1}C_r$$

ex) NCT 멤버 중 7명을 뽑아 유닛 그룹을 만드는 경우의 수는?

$$_{23}C_7 = {23! \over (23 - 7)!7!} = 245,157$$

<br>

### 순열/조합 개수 구하기 (math 모듈)

- `math.perm(n, r)`

  n개 중 r개를 뽑아서 정렬하는 **순열의 개수**를 리턴한다.

- `math.comb(n, r)`

  n개 중 r개를 뽑는 **조합의 개수**를 리턴한다.

```python

import math

# n개 중 r개를 뽑아서 정렬하는 순열의 개수 출력
a = math.perm(n, r)
print(a)

# n개 중 r개를 뽑는 조합의 개수 출력
b = math.comb(n, r)
print(b)

# n개 중 r개를 중복을 허용하여 뽑는 중복 조합의 개수 출력
c = math.comb(n + r - 1, r)
print(c)
```

<br>

### 순열/조합 모두 나열하기 (itertools 모듈)


- `itertools.permutations(iter, n)`

  이터레이터가 내놓는 원소들로부터 만들어낸 길이 n의 **순열**을 전부 리턴한다.

- `itertools.combinations(iter, n)`

  이터레이터가 내놓는 원소들로부터 만들어낸 길이 n의 **조합**을 전부 리턴한다.

- `itertools.combinations_with_replacement(iter, n)`

  이터레이터가 내놓는 원소들로부터 만들어낸 길이 n의 **중복 조합**을 전부 리턴한다.

```python

import itertools


it = itertools.permutations([1, 2, 3], 2)
print(list(it))

>>> [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]

it = itertools.combinations([1, 2, 3], 2)
print(list(it))

>>> [(1, 2), (1, 3), (2, 3)]

it = itertools.combinations_with_replacement([1, 2, 3], 2)
print(list(it))

>>> [(1, 1), (1, 2), (1, 3), (2, 2), (2, 3)]
```

<br>

### 관련 문제

- [백준 N과 M 시리즈](https://www.acmicpc.net/workbook/view/2052)

- [백준 10974번: 모든 순열](https://www.acmicpc.net/problem/10974)

- [백준 1182번: 부분수열의 합](https://www.acmicpc.net/problem/1182)

- [백준 1759번: 암호 만들기](https://www.acmicpc.net/problem/1759)

