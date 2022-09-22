"""
정확성 테스트 통과, 효율성 테스트 9개중 5개 통과
"""

from collections import deque


def shift_row(rc):
    arr = rc.pop()
    rc.appendleft(arr)


def rotate(rc, R, C):
    rc[R].append(rc[R - 1][C])

    for r in range(R - 1, 0, -1):
        rc[r][C] = rc[r - 1][C]

    rc[0].appendleft(rc[1][0])

    for r in range(1, R):
        rc[r][0] = rc[r + 1][0]

    rc[0].pop()
    rc[R].popleft()


def solution(rc, operations):
    R = len(rc) - 1
    C = len(rc[0]) - 1

    rc = deque([deque(arr) for arr in rc])

    for operation in operations:
        if operation[0] == "S":
            shift_row(rc)
        else:
            rotate(rc, R, C)

    return [list(arr) for arr in rc]
