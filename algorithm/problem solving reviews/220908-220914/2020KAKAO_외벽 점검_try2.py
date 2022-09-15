"""
공식 해설 (https://tech.kakao.com/2019/10/02/kakao-blind-recruitment-2020-round1/) 읽은 후 다시 풀이
"""

from itertools import permutations


def solution(n, weak, dist):
    W, D = len(weak), len(dist)

    for w in range(W - 1):
        weak.append(weak[w] + n)

    dist.sort(reverse=True)

    for count in range(1, D + 1):
        for start_idx in range(W):
            cnt_location = weak[start_idx]
            cnt_idx = start_idx
            end_idx = start_idx + W - 1

            for distance_set in permutations(dist[:count], count):
                for distance in distance_set:

                    while cnt_idx <= end_idx and weak[cnt_idx] <= cnt_location + distance:
                        cnt_idx += 1

                    if cnt_idx > end_idx:
                        return count

                    cnt_location = weak[cnt_idx]

                cnt_idx = start_idx
                cnt_location = weak[cnt_idx]

    return -1


print(solution(12, [1, 5, 6, 10], [1, 2, 3, 4]))
print(solution(12, [1, 3, 4, 9, 10], [3, 5, 7]))
