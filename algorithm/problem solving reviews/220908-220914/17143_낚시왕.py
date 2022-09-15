from sys import stdin


# 방향 조정
new_d = [-1, 0, 2, 1, 3]

# 상우하좌
dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]


def catch_shark(cnt):
    """
    Args:
        cnt: 낚시왕의 열 위치
    """
    global R, total_size, board

    for r in range(R):
        if board[r][cnt] != -1:
            shark_num = board[r][cnt]
            total_size += sizes[shark_num]
            board[r][cnt] = -1
            break


def get_distance_from_wall(r, c, d):
    """
    Returns:
        [현재 이동 방향 기준으로 벽으로부터의 길이, 벽과 벽 사이의 길이]
    """
    global R, C

    if d == 0:
        return [r, R - 1]
    elif d == 1:
        return [C - c - 1, C - 1]
    elif d == 2:
        return [R - r - 1, R - 1]
    else:
        return [c, C - 1]


def move_shark(r, c, shark_num):
    """
    Args:
        r, c: 상어의 이동 전 위치
        shark_num: 상어의 번호
    Returns:
        r, c: 이동 후의 상어의 위치
    """
    s, d = speeds[shark_num], directions[shark_num]
    distance, full = get_distance_from_wall(r, c, d)

    # 1. 벽에 닿지 않는 경우
    if distance > s:
        return r + (dr[d] * s), c + (dc[d] * s)
    # 2. 벽에는 닿지만 반대쪽 벽에 다시 닿지는 않는 경우
    elif distance <= s < distance + full:
        # 이동 방향을 반대로 바꾼다.
        d = (d + 2) % 4
        directions[shark_num] = d

        if d % 2 == 0:
            r = walls[d] + (dr[d] * (s - distance))
        else:
            c = walls[d] + (dc[d] * (s - distance))

        return r, c
    # 3. 벽에 닿은 뒤, 반대쪽 벽에 다시 닿는 경우
    else:
        # 0: R - 1 / 1: 0 / 2: 0 / 3: C - 1

        if d % 2 == 0:
            r = walls[d] + (dr[d] * (s - distance - full))
        else:
            c = walls[d] + (dc[d] * (s - distance - full))

        return r, c


def move_total_shark():
    global board, R, C
    new_locations = []

    for r in range(R):
        for c in range(C):
            if board[r][c] != -1:
                new_r, new_c = move_shark(r, c, board[r][c])
                new_locations.append([new_r, new_c, board[r][c]])
                board[r][c] = -1

    for new_r, new_c, shark_num in new_locations:
        if board[new_r][new_c] == -1:
            board[new_r][new_c] = shark_num
        else:
            new_size = sizes[shark_num]
            second_size = sizes[board[new_r][new_c]]

            if new_size > second_size:
                board[new_r][new_c] = shark_num


R, C, M = map(int, stdin.readline().split())
board = [[-1] * C for _ in range(R)]
speeds = []
directions = []
sizes = []
total_size = 0

# 현재 이동 방향의 반대편 벽의 좌표
walls = [R - 1, 0, 0, C - 1]

for idx in range(M):
    r, c, s, d, z = map(int, stdin.readline().split())
    d = new_d[d]

    if d % 2 == 0:  # 이동 방향이 상하인 경우
        s %= (2 * R - 2)
    else:           # 이동 방향이 좌우인 경우
        s %= (2 * C - 2)

    board[r - 1][c - 1] = idx
    speeds.append(s)
    directions.append(d)
    sizes.append(z)

for current in range(C):
    # 1. 낚시왕이 상어를 잡는다.
    catch_shark(current)

    # 2. 상어들이 이동한다.
    move_total_shark()

print(total_size)
