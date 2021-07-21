# 단축 평가 (short-circuit evaluation)

> 논리 연산자의 반환값을 판별할 때,
>
> 첫 번째 값만 보고도 반환값을 알 수 있는 경우
>
> 두 번째 값은 확인하지 않고 첫 번째 값을 반환하는 것



### and 연산

- `A and B`에서 A가 False라면, `A and B`의 반환값은 무조건 False이므로, A를 반환

  ```python
  a = 0 and 5
  print(a)
  
  # 0
  ```

- `A and B`에서 A가 True라면, `A and B`의 반환값은 B의 반환값과 같으므로, B를 반환

  ```python
  b = 8 and 3
  print(b)
  
  # 3
  ```

  

### or 연산

- `A or B`에서 A가 True라면, `A or B`의 반환값은 무조건 True이므로, A를 반환

  ```python
  a = 17 or 0
  print(a)
  
  # 17
  ```

- `A or B`에서 A가 False라면, `A or B`의 반환값은 B의 반환값과 같으므로, B를 반환

  ```python
  b = 0 or 5
  print(b)
  
  # 5
  ```



### 활용

- 단축 평가를 활용하면 컴퓨터가 계산하는 양을 줄일 수 있다.
  - `A and B`에서는 False일 확률이 더 높은 객체를 `and` 앞에 두는 것이 좋다.
  - `A or B`에서는 True일 확률이 더 높은 객체를 `or` 앞에 두는 것이 좋다.