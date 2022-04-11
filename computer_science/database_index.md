# INDEX

> 데이터베이스의 인덱스



### What : index란 무엇인가

위키피디아에서 정의하는 데이터베이스 인덱스는 아래와 같다.

> A **database index** is a [data structure](https://en.wikipedia.org/wiki/Data_structure) that improves the speed of data retrieval operations on a [database table](https://en.wikipedia.org/wiki/Table_(database)) at the cost of additional writes and storage space to maintain the index data structure.
>
> 출처 : https://en.wikipedia.org/wiki/Database_index



이를 다시 2가지 부분으로 나누어 보자.

1. A database index is a data structure that improves the speed of data retrieval operations on a database table

- **인덱스를 사용하는 이유**에 대한 설명이다. 인덱스는 데이터베이스 테이블에서 데이터 검색 속도를 향상시키는 자료구조다.

2. at the cost of additional writes and storage space to maintain the index data structure

- **인덱스의 단점**에 대한 설명이다. 인덱스가 데이터 검색 속도를 향상시키는 대가로 희생하는 것은, 추가적인 쓰기 작업과 저장 공간이다.



결국 인덱스를 잘 사용하기 위해서는 검색 속도 향상의 효과가 크고, 추가적인 오버헤드가 적은 방식으로 사용해야 한다.

<br>

### When : index는 언제 쓰는 게 좋은가?

인덱스를 사용하면 검색 속도가 향상된다. 하지만 이를 위해 정렬된 상태를 유지하기 때문에, 삽입/삭제/수정을 하는 경우 추가적인 오버헤드가 발생한다. 



**SELECT**

- 조건절(WHERE)과 함께 쓰이는 경우 성능이 향상된다. 인덱스가 있으면 원하는 데이터에 빠르게 접근 가능하기 때문이다.

**INSERT** 

- 배열 자료구조에서 INSERT의 시간 복잡도는 `O(n)`이다. 중간에 값이 삽입된 경우, 그 다음부터 마지막 값까지 모두 한칸씩 뒤로 움직여야 하기 때문이다. 
- 위와 같은 이유로 INSERT문 수행시 인덱스는 성능을 저하시킨다. 인덱스가 없다면, 그냥 새로운 값을 마지막에 추가하면 될 것이다. 하지만 인덱스는 정렬된 상태를 유지하므로 새로운 데이터는 중간에 삽입될 수 있고, 이러한 경우 추가적인 작업이 발생한다.

**DELETE**

- 데이터 검색 속도가 빨라지므로, 삭제할 데이터에 접근하는 시간 자체는 줄어든다.

- DELETE시 index 데이터는 삭제되는 대신, '사용하지 않음'을 표시한다. 만약 실제 사용하는 데이터에 비해 사용하지 않는 데이터가 너무 많아진다면, 공간을 낭비할 수 있으며 이후 검색 속도에 악영향을 줄 수 있다. 

**UPDATE**

- UPDATE시에도 해당 데이터를 바로 수정하는 대신, 기존 인덱스를 '사용하지 않음' 표시한 뒤 새로운 인덱스를 INSERT한다. DELETE + INSERT이므로 공간 낭비와 성능 저하가 발생할 수 있다.

<br>

### Where : 어떤 column에서 index를 사용해야 하는가?

- 조건절(WHERE)에 자주 사용되는 경우
  - 인덱스 사용시 검색 속도가 향상되기 때문이다.
- 중복이 적은 경우
  - 100만 명의 회원 데이터에서, 성별을 인덱스로 설정한다면 매우 비효율적일 것이다.

- ORDER BY에 자주 사용되는 경우
  - 인덱스는 정렬된 상태를 유지하기 때문이다.
- INSERT/UPDATE/DELETE에 자주 사용되지 **않는** 경우
  - 위에서 본 것처럼, DML에서는 오히려 성능 저하를 초래할 수 있기 때문이다.

<br>

### How : index는 어떤 자료구조로 구현되어 있는가

- mongoDB의 경우, b-tree 자료구조를 사용한다.

- mySQL의 경우, b+tree 자료구조를 사용하는데, 이는 b-tree의 확장된 개념이다.



**b-tree 자료구조**

- 자식 트리의 밸런스를 유지하는 balanced tree의 일종
- 이진 탐색 트리와 달리, 최악의 경우에도 시간복잡도가 `O(logN)`이다.



Q. 해시 테이블의 탐색 시간은 `O(1)`인데, 왜 b-tree 자료구조를 사용했을까?

A. 해시 테이블의 경우 값이 정렬되어 있지 않다. 따라서 범위 내의 값을 검색하거나, 정렬된 결과를 가져오는 데 사용할 수 없다.

회원정보 테이블에서 나이를 인덱스로 설정했다고 하자. (물론 이는 별로 좋지 않은 선택일 것이다.) 인덱스를 해시 테이블로 구현할 경우, 나이가 24살인 회원은 매우 빠르게 찾을 수 있다. 하지만 나이가 30대인 회원을 찾거나, 나이가 많은 순으로 10명의 회원을 찾는 데 있어서는 인덱스의 도움을 받지 못할 것이다.

<br>

### 참고 자료

https://en.wikipedia.org/wiki/Database_index

https://helloinyong.tistory.com/296