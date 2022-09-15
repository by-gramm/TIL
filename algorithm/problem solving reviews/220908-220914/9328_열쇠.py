from sys import stdin
from collections import deque
import string


dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]

T = int(stdin.readline())

for _ in range(T):
    h, w = map(int, stdin.readline().split())
    board = []
    visited = [[False] * (w + 2) for _ in range(h + 2)]
    total_count = 0

    board.append(['.'] * (w + 2))
    for _ in range(h):
        board.append(['.'] + [x for x in stdin.readline().rstrip()] + ['.'])
    board.append(['.'] * (w + 2))

    key_set = set([x for x in stdin.readline().rstrip()])

    if '0' in key_set:
        key_set.remove('0')

    # 초기 열쇠로 열 수 있는 문들을 열어둔다.
    for r in range(1, h + 1):
        for c in range(1, w + 1):
            if board[r][c].lower() in key_set:
                board[r][c] = '.'

    queue = deque()
    queue.append([r, c])
    ready_queue = dict()
    for char in string.ascii_uppercase:
        ready_queue[char] = []

    while queue:
        r, c = queue.popleft()

        for i in range(4):
            nr, nc = r + dr[i], c + dc[i]

            if 0 <= nr < h + 2 and 0 <= nc < w + 2 and not visited[nr][nc]:
                visited[nr][nc] = True

                if board[nr][nc] == '.':
                    queue.append([nr, nc])
                elif board[nr][nc] == '$':
                    # board[nr][nc] = '.'
                    total_count += 1
                    queue.append([nr, nc])
                elif 'a' <= board[nr][nc] <= 'z':
                    queue.append([nr, nc])

                    # 새로운 열쇠를 발견한 경우, 해당 열쇠로 열 수 있는 문들을 연다.
                    if board[nr][nc] not in key_set:
                        key_set.add(board[nr][nc])

                        for saved_r, saved_c in ready_queue[board[nr][nc].upper()]:
                            queue.append([saved_r, saved_c])
                elif 'A' <= board[nr][nc] <= 'Z':
                    if board[nr][nc].lower() in key_set:
                        queue.append([nr, nc])
                    else:
                        ready_queue[board[nr][nc]].append([nr, nc])

    print(total_count)
