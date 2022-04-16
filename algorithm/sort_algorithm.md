# 정렬 알고리즘



**가장 좋은 정렬 알고리즘은 무엇일까?**  삽입 정렬, 버블 정렬, 힙 정렬, 퀵 정렬 등 다양한 정렬 알고리즘에 대해 배웠음에도, 이 질문에 대해 답할 수 없었다. 그래서 실제로 프로그래밍 언어에서 정렬을 어떻게 구현하는지 조사하여, 질문에 대한 답을 나름대로 정리해보았다.

<br>

### Quick Sort

일반적으로 가장 빠른 정렬 알고리즘으로 알려진 것은 **quick sort**다. (이름부터 그렇다.) 퀵 정렬은 아래의 단계로 이루어진다.

1. 리스트에서 하나의 요소를 **피벗(pivot)**으로 정한다.
2. 피벗을 기준으로 피벗보다 작은 요소는 모두 피벗 왼쪽으로, 피벗보다 큰 요소는 모두 피벗 오른쪽에 몰아넣는다.
3. 피벗을 제외한 왼쪽 리스트와 오른쪽 리스트를 같은 방식으로 정렬한다. (Divide and conquer)

퀵 정렬은 대개의 경우 매우 빠르지만, 최악의 경우 `O(n^2)`의 시간복잡도를 가진다. 

[10, 9, 8, 7, 6, 5, 4, 3, 2, 1]을 가장 왼쪽 수를 피벗으로 고르는 퀵 정렬로 정렬한다고 하자. 처음 피벗은 10이고, 피벗 왼쪽에 [9, 8, 7, 6, 5, 4, 3, 2, 1]이 들어간다. 다시 피벗의 왼쪽 리스트에서 9가 피벗이 되고, 피벗 9의 왼쪽에 [8, 7, 6, 5, 4, 3, 2, 1]이 들어간다. 다시 8이 피벗이 되고...

위의 경우처럼 퀵 정렬은 비효율적인 알고리즘이 될 수도 있다. 따라서 퀵 정렬에서는 피벗의 선택 기준이 중요하다. 이상적으로는 리스트의 중위수(median)을 피벗으로 삼는 것이 좋다.

<br>

### Dual-pivot Quick Sort

Java의 `Arrays.sort()`에서 기본형 타입의 배열은 **DualPivotQuickSort** 클래스의 `sort()` 메서드를 사용한다. 이는 이름처럼 피벗 2개를 사용한 퀵 정렬이다. DualPivotQuickSort 클래스의 주석에 따르면, dual-pivot quick sort는

- 피벗이 하나인 퀵 정렬에서 시간 복잡도가 `O(n^2)`이 되는 많은 경우에도 `O(nlogn)`의 시간 복잡도로 정렬을 수행하며, 
- 피벗이 하나인 퀵 정렬보다 일반적으로 더 빠르다.

퀵 정렬 자체가 이미 빠른데, dual-pivot quick sort는 퀵 정렬보다 더 빠르고, 퀵 정렬의 단점까지 보완한다. 그렇다면 이 성능 좋은 정렬이 곧 최선의 정렬 알고리즘일까?

하지만 `Arrays.sort()`에서 참조형 타입의 배열은 **tim sort**를 사용한다. Java의 `Collections.sort()`의 경우, 내부에서 리스트를 Object 배열로 만들어 `Arrays.sort()`로 보내기 때문에 마찬가지로 tim sort를 사용한다. 파이썬에서는 `sort()`와 `sorted()` 모두 tim sort를 사용한다. 이처럼 많은 정렬 메서드에서 quick sort 대신 tim sort를 사용하는 이유는 무엇일까?

<br>

### stable sort vs unstable sort

quick sort는 tim sort와 달리 비안정(unstable) 정렬이기 때문이다. 

**안정 정렬**은 중복된 값을 입력 순서와 동일하게 정렬함을 보장한다. 반면 **비안정 정렬**은 이를 보장하지 않는다.

기본형 타입의 경우 변수는 값 자체를 저장한다. 그래서 중복된 값의 순서가 바뀌더라도, 값 자체는 그대로이기 때문에 아무런 상관이 없다. (값이 동일한 두 기본형 타입은 구분할 수 없다.) 그래서 성능이 좋은 dual-pivot quick sort를 사용한다.

반면 참조형 타입의 경우 값 자체가 아니라 메모리 주소값을 저장한다. 같은 값을 가진 두 객체가 다른 메모리 주소에 저장될 수 있다. 값은 같지만 주소는 다른 두 객체의 순서가 달라지면 문제가 발생할 수도 있다. 그래서 안정 정렬 알고리즘인 tim sort를 사용한다.

파이썬에는 기본형 타입 자체가 없다. 모든 것이 다 Object다. 따라서 안정 정렬인 tim sort를 사용한다. 

<br>

### Tim sort

tim sort는 **삽입 정렬**과 **병합 정렬**이 결합된 정렬 알고리즘이다. 아래와 같은 순서로 이루어진다.

1. 데이터를 Run이라는 단위로 나눈다. Run의 길이는 전체 원소의 개수가 N일 때, `min(N, 2^5 ~ 2^6)`으로 정의한다.
2. 각 Run을 삽입 정렬(정확히는 이진 삽입 정렬)로 정렬한다.
3. 정렬된 각 Run을 병합한다.



tim sort에 대한 자세한 내용은 아래 링크들을 참고하면 좋다.

[Naver D2 - Tim sort에 대해 알아보자](https://d2.naver.com/helloworld/0315536)

[Wikipedia - Timsort](https://en.wikipedia.org/wiki/Timsort)

<br>

### Counting Sort

위 내용을 바탕으로 안정 정렬 중에서는 tim sort가, 비안정 정렬 중에서는 quick sort가 가장 좋은 알고리즘이라는 결론을 내릴 수 있다. 하지만 특수한 경우에 **계수 정렬(counting sort)**은 tim sort나 quick sort보다 훨씬 효율적인 정렬 알고리즘이 된다.

계수 정렬은 이름 그대로 각 요소의 개수를 세서 정렬하는 방식이다. 0~99 사이의 수 100만 개를 정렬한다고 하자. 정렬할 데이터를 한번 순회하면서 길이가 100인 배열 counts의 counts[i]에 i의 개수를 저장한다. 그리고 0부터 99까지 counts에 저장된 개수만큼 이어붙이기만 하면 된다.

계수 정렬은 **데이터의 개수에 비해 데이터의 범위가 작을 때** 강력한 효과를 발휘한다. 실제로 java에서도 제한적으로 계수 정렬을 사용한다.

앞서 Java의 `Arrays.sort()`에서 기본형 타입의 배열은 DualPivotQuickSort 클래스의 `sort()` 메서드를 사용함을 알아보았다. 그런데 사실 DualPivotQuickSort 클래스의 `sort()`가 반드시 피벗 2개를 사용한 퀵 정렬을 사용하지는 않는다. 자료형 및 배열의 길이에 따라 계수 정렬, 삽입 정렬, 병합 정렬 등이 다양하게 사용된다.

```java
/**
 * If the length of an array to be sorted is less than this
 * constant, Quicksort is used in preference to merge sort.
 */
private static final int QUICKSORT_THRESHOLD = 286;

/**
 * If the length of an array to be sorted is less than this
 * constant, insertion sort is used in preference to Quicksort.
 */
private static final int INSERTION_SORT_THRESHOLD = 47;

/**
 * If the length of a byte array to be sorted is greater than this
 * constant, counting sort is used in preference to insertion sort.
 */
private static final int COUNTING_SORT_THRESHOLD_FOR_BYTE = 29;

/**
 * If the length of a short or char array to be sorted is greater
 * than this constant, counting sort is used in preference to Quicksort.
 */
private static final int COUNTING_SORT_THRESHOLD_FOR_SHORT_OR_CHAR = 3200;

(코드 출처 : https://github.com/frohoff/jdk8u-dev-jdk/blob/master/src/share/classes/java/util/DualPivotQuicksort.java)
```

위 내용 중 **계수 정렬(counting sort)**에 대한 부분만 살펴보면, 

- byte 배열의 길이가 29보다 크거나
- short/char 배열의 길이가 3200보다 큰 경우

계수 정렬이 사용된다. 



- **byte**는 최소값이 -128, 최대값이 127로, 가능한 값이 총 256개다. 
- **short**는 최소값이 -32768, 최대값이 32767로, 가능한 값이 총 65536개다.
- **char**는 최소값이 0, 최대값이 65535로, 가능한 값은 총 65536개다.



앞서 말했듯이 계수 정렬은 **데이터의 개수에 비해 데이터의 범위가 작을 때** 효과적이다. java에서는 그 기준을 범위가 256개일 때는 배열 길이가 29보다 클 때, 범위가 65536개일 때는 배열 길이가 3200보다 클 때로 설정했다.

<br>

### 정리

데이터의 길이, 범위, 정렬된 정도 등에 따라 효과적인 정렬 알고리즘은 다르다. 정렬 알고리즘 중 대체로 성능이 가장 좋은 것은 **quick sort**이다. 단, quick sort는 최악의 경우 시간복잡도가 `O(n^2)`이 될 수 있는데, 이를 보완한 것이 **dual-pivot quick sort**다. 그런데 quick sort는 unstable하다. 그래서 많은 프로그래밍 언어의 내장 정렬 메서드에서는 stable한 **tim sort**를 사용한다. 한편 **counting sort**는 데이터의 개수에 비해 데이터의 범위가 작을 때 제한적으로 효과적이다. 

<br>

### 참고 자료

https://github.com/frohoff/jdk8u-dev-jdk/blob/master/src/share/classes/java/util/DualPivotQuicksort.java

https://stackoverflow.com/questions/3707190/why-does-javas-arrays-sort-method-use-two-different-sorting-algorithms-for-diff

https://www.geeksforgeeks.org/know-sorting-algorithm-set-1-sorting-weapons-used-programming-languages/

https://d2.naver.com/helloworld/0315536

https://en.wikipedia.org/wiki/Timsort