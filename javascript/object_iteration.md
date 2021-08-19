# 자바스크립트 객체 순회

자바스크립트 객체를 순회하는 방법을 정리해보았다. 그런데 이제 파이썬을 곁들인.

<br>

### 1. key값으로 순회

- 방법 1 : `Object.keys(obj)`로 순회

```javascript
const scores = {'가영': 80, '나영': 70, '다영': 100};

for (let name of Object.keys(scores)) {
  console.log(name);
}

// 가영
// 나영
// 다영
```

- 방법 2 : `for ~ in` 문으로 순회

```javascript
for (let name in scores) {
  console.log(name);
}

// 가영
// 나영
// 다영
```

참고) 파이썬의 딕셔너리 key값으로 순회하기

```python
scores = {'가영': 80, '나영': 70, '다영': 100}

# 방법 1 : dict.keys()로 순회하기
for name in scores.keys():
    print(name)

# 방법 2 : for문으로 순회하기
for name in scores:
    print(name)
```

<br>

### 2. value값으로 순회

- 방법 1 : `Object.keys(obj)`로 순회하면서 키 값을 다시 객체에 대입하기

```javascript
for (let name of Object.keys(scores)) {
  console.log(scores[name]);
}

// 80
// 70
// 100
```

- 방법 2 : `Object.values(obj)`로 순회하기

```javascript
for (let score of Object.values(scores)) {
  console.log(score);
}

// 80
// 70
// 100
```

참고) 파이썬의 딕셔너리 value값으로 순회하기

```python
scores = {'가영': 80, '나영': 70, '다영': 100}

# 방법 1: dict.keys()로 순회하면서 키 값을 다시 딕셔너리에 대입하기
for name in scores.keys():
    print(scores[name])

# 방법 2: dict.values()로 순회하기
for score in scores.values():
    print(score)
```

<br>

### 3. key, value 동시에 순회하기

- `Object.entries(obj)`로 순회하기

```javascript
for (let [name, score] of Object.entries(scores)) {
  console.log(`이름: ${name} | 성적: ${score}`);
}

// 이름: 가영 | 성적: 80
// 이름: 나영 | 성적: 70
// 이름: 다영 | 성적: 100
```

참고) 파이썬의 딕셔너리 key, value 동시에 순회하기

```python
scores = {'가영': 80, '나영': 70, '다영': 100}

# dict.items()로 순회하기
for name, score in scores.items():
    print(f"이름: {name} | 성적: {score}")
```
