from sys import stdin


def get_min_cost(board, N, M):
    for c in range(sum(costs) + 1):
        for r in range(N):
            if board[r][c] >= M:
                return c


N, M = map(int, stdin.readline().split())
memory_bytes = [int(x) for x in stdin.readline().split()]
costs = [int(x) for x in stdin.readline().split()]

# board[r][c]: r번 앱까지 고려했을 때 c원으로 절약 가능한 메모리
board = [[0] * (sum(costs) + 1) for _ in range(N)]
board[0][costs[0]] = memory_bytes[0]

for r in range(1, N):
    cnt_cost = costs[r]
    board[r][cnt_cost] = memory_bytes[r]

    for c in range(sum(costs) + 1):
        if board[r - 1][c] > 0:
            board[r][c] = max(board[r - 1][c], board[r][c])
            board[r][c + cnt_cost] = max(board[r][c + cnt_cost], board[r - 1][c] + memory_bytes[r])

print(get_min_cost(board, N, M))
