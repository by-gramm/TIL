from sys import stdin


def get_max_count(cnt_count, diff):
    """
    Args:
        cnt_count: 현재까지 놓은 비숍의 개수
        diff: 현재 탐색중인 r-c의 값
    """
    global board, N, max_count

    if cnt_count + N - diff <= max_count:
        return

    if diff > (N - 1):
        max_count = max(max_count, cnt_count)
        return

    if diff >= 0:
        max_r, min_r = N, diff
    else:
        max_r, min_r = diff + N, 0

    for r in range(min_r, max_r):
        c = r - diff

        if board[r][c] and not r_plus_c_visited[r + c]:
            r_plus_c_visited[r + c] = True
            get_max_count(cnt_count + 1, diff + 1)
            r_plus_c_visited[r + c] = False

    get_max_count(cnt_count, diff + 1)


N = int(stdin.readline())
board = []
max_count = 0
r_plus_c_visited = [False] * (2 * N - 1)   # 0 ~ (2N - 2)

for _ in range(N):
    board.append([int(x) for x in stdin.readline().split()])

get_max_count(0, 1 - N)
print(max_count)
