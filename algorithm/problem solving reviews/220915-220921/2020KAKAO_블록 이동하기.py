from collections import deque
from math import inf


def get_garo_movables(board, r, c):
    movables = []

    if not board[r][c - 1]:
        movables.append([1, r, c - 1])
    if not board[r][c + 2]:
        movables.append([1, r, c + 1])
    if not (board[r - 1][c] or board[r - 1][c + 1]):
        movables.append([1, r - 1, c])
        movables.append([0, r - 1, c])
        movables.append([0, r - 1, c + 1])
    if not (board[r + 1][c] or board[r + 1][c + 1]):
        movables.append([1, r + 1, c])
        movables.append([0, r, c])
        movables.append([0, r, c + 1])

    return movables


def get_sero_movables(board, r, c):
    movables = []

    if not board[r - 1][c]:
        movables.append([0, r - 1, c])
    if not board[r + 2][c]:
        movables.append([0, r + 1, c])
    if not (board[r][c - 1] or board[r + 1][c - 1]):
        movables.append([0, r, c - 1])
        movables.append([1, r, c - 1])
        movables.append([1, r + 1, c - 1])
    if not (board[r][c + 1] or board[r + 1][c + 1]):
        movables.append([0, r, c + 1])
        movables.append([1, r, c])
        movables.append([1, r + 1, c])

    return movables


def solution(board):
    N = len(board)

    new_board = [[1] * (N + 2)]
    for i in range(N):
        new_board.append([1] + board[i] + [1])
    new_board.append([1] * (N + 2))

    garo_distances = [[inf] * (N + 2) for _ in range(N + 2)]
    sero_distances = [[inf] * (N + 2) for _ in range(N + 2)]
    garo_distances[1][1] = 0

    queue = deque()
    queue.append([1, 1, 1, 0])  # 가로, r=1, c=1

    while queue:
        d, r, c, distance = queue.popleft()

        if d == 1:
            movables = get_garo_movables(new_board, r, c)
        else:
            movables = get_sero_movables(new_board, r, c)

        for cnt_d, cnt_r, cnt_c in movables:
            if cnt_d == 1:
                if cnt_r == N and cnt_c == (N - 1):
                    return distance + 1

                if distance + 1 < garo_distances[cnt_r][cnt_c]:
                    garo_distances[cnt_r][cnt_c] = distance + 1
                    queue.append([cnt_d, cnt_r, cnt_c, distance + 1])

            if cnt_d == 0:
                if cnt_r == (N - 1) and cnt_c == N:
                    return distance + 1

                if distance + 1 < sero_distances[cnt_r][cnt_c]:
                    sero_distances[cnt_r][cnt_c] = distance + 1
                    queue.append([cnt_d, cnt_r, cnt_c, distance + 1])


solution([[0, 0, 0, 1, 1],[0, 0, 0, 1, 0],[0, 1, 0, 1, 1],[1, 1, 0, 0, 1],[0, 0, 0, 0, 0]])
