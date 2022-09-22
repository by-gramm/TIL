from collections import deque

dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]


def is_valid_point(r, c):
    return (0 <= r <= 3) and (0 <= c <= 3)


def is_all_found(board):
    for r in range(4):
        for c in range(4):
            if board[r][c]:
                return False
    return True


def get_num_count(board):
    num_set = set()

    for r in range(4):
        for c in range(4):
            num_set.add(board[r][c])

    return len(num_set) - 1


def get_search_points(board, r, c):
    points = []

    for i in range(4):
        nr, nc = r + dr[i], c + dc[i]

        if is_valid_point(nr, nc):
            points.append([nr, nc])

            if not board[nr][nc] and is_valid_point(nr + dr[i], nc + dc[i]):
                nr, nc = nr + dr[i], nc + dc[i]

                # CASE1. 2칸이 벽의 끝 / 2번째 칸이 빈칸     => Ctrl로 이동시 2칸
                # CASE2. 2칸이 벽의 끝 / 2번째 칸에 카드     => Ctrl로 이동시 2칸
                # CASE3. 3칸이 벽의 끝 / 2번째 칸에 카드     => Ctrl로 이동시 2칸
                if not is_valid_point(nr + dr[i], nc + dc[i]) or board[nr][nc]:
                    points.append([nr, nc])
                    continue

                # CASE4. 3칸이 벽의 끝 / 3번째 칸에 카드     => Ctrl로 이동시 3칸
                # CASE5. 3칸이 벽의 끝 / 2, 3번째 칸이 빈칸  => Ctrl로 이동시 3칸
                points.append([nr + dr[i], nc + dc[i]])

    return points


def find_same_number(board, r, c, target):
    counts = [[1234] * 4 for _ in range(4)]
    counts[r][c] = 0
    queue = deque()
    queue.append([r, c, 0])

    while queue:
        cnt_r, cnt_c, count = queue.popleft()

        for nr, nc in get_search_points(board, cnt_r, cnt_c):
            if counts[nr][nc] == 1234:
                if board[nr][nc] == target:
                    return nr, nc, count + 1

                counts[nr][nc] = count + 1
                queue.append([nr, nc, count + 1])


def get_min_count(board, r, c, cnt_count):
    if is_all_found(board):
        return cnt_count

    min_count = 12345

    counts = [[1234] * 4 for _ in range(4)]
    counts[r][c] = 0
    queue = deque()
    queue.append([r, c, 0])

    # 시작 위치에 카드가 있는 경우 예외 처리
    if not cnt_count and board[r][c]:
        next_r, next_c, rest = find_same_number(board, r, c, board[r][c])
        found_num = board[r][c]

        board[r][c] = 0
        board[next_r][next_c] = 0

        result = get_min_count(board, next_r, next_c, cnt_count + rest)
        min_count = min(min_count, result)

        board[r][c] = found_num
        board[next_r][next_c] = found_num

    while queue:
        cnt_r, cnt_c, count = queue.popleft()

        for nr, nc in get_search_points(board, cnt_r, cnt_c):
            if counts[nr][nc] == 1234:
                counts[nr][nc] = count + 1
                queue.append([nr, nc, count + 1])

                if board[nr][nc]:
                    next_r, next_c, rest = find_same_number(board, nr, nc, board[nr][nc])
                    total_count = count + rest + 1
                    found_num = board[nr][nc]

                    board[nr][nc] = 0
                    board[next_r][next_c] = 0

                    result = get_min_count(board, next_r, next_c, cnt_count + total_count)
                    min_count = min(min_count, result)

                    board[nr][nc] = found_num
                    board[next_r][next_c] = found_num

    return min_count


def solution(board, r, c):
    return get_min_count(board, r, c, 0) + get_num_count(board) * 2


print(solution([[1,0,0,3],[2,0,0,0],[0,0,0,2],[3,0,1,0]], 1, 0))
print(solution([[3,0,0,2],[0,0,1,0],[0,1,0,0],[2,0,0,3]], 0, 1))
