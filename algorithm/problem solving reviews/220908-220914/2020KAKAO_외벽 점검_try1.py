"""
해설 보기 전 풀이 => 테스트 케이스 25개 중 16개 통과
"""
global visited, min_count


def get_min_count(current, W, D, weak, dist, n):
    global visited, min_count
    count = D - 1 - current

    if count >= min_count:
        return

    # 모든 곳을 다 방문한 경우
    if sum([int(x) for x in visited]) == W:
        min_count = count
        return

    # 더 이상 투입할 인원이 없는 경우
    if current < 0:
        return

    distance = dist[current]

    for idx in range(W):
        if not visited[idx]:
            end_weak = weak[idx] + distance
            visit_idxs = [idx]
            visited[idx] = True

            for _ in range(W - 1):
                idx += 1

                if idx >= W:
                    if weak[idx - W] + n > end_weak:
                        break
                    visited[idx - W] = True
                    visit_idxs.append(idx - W)
                else:
                    if weak[idx] > end_weak:
                        break
                    visited[idx] = True
                    visit_idxs.append(idx)

            get_min_count(current - 1, W, D, weak, dist, n)

            for v in visit_idxs:
                visited[v] = False


def solution(n, weak, dist):
    global visited, min_count
    W, D = len(weak), len(dist)
    visited = [False] * W
    dist.sort()
    min_count = 12345

    get_min_count(D - 1, W, D, weak, dist, n)

    if min_count == 12345:
        return -1

    return min_count


print(solution(12, [1, 5, 6, 10], [1, 2, 3, 4]))
print(solution(12, [1, 3, 4, 9, 10], [3, 5, 7]))
