"""
Python 3으로는 시간초과
PyPy3으로는 5420ms
"""

from sys import stdin


N = int(stdin.readline())
total_count = 0

c_visited = [False] * N
r_minus_c_visited = [False] * (2 * N - 1)  # (1 - N) ~ (N - 1)
r_plus_c_visited = [False] * (2 * N - 1)   # 0 ~ (2N - 2)


def count_nqueen(cnt_r):
    global N, total_count

    # if cnt_r == N:
    #     total_count += 1
    #     return

    for c in range(N):
        r_plus_c = cnt_r + c
        r_minus_c = cnt_r - c + N - 1
        if not (c_visited[c]
                or r_plus_c_visited[r_plus_c]
                or r_minus_c_visited[r_minus_c]):

            if cnt_r == N - 1:
                total_count += 1
                return

            c_visited[c] = True
            r_plus_c_visited[r_plus_c] = True
            r_minus_c_visited[r_minus_c] = True

            count_nqueen(cnt_r + 1)

            c_visited[c] = False
            r_plus_c_visited[r_plus_c] = False
            r_minus_c_visited[r_minus_c] = False


count_nqueen(0)
print(total_count)


