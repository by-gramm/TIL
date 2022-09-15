def is_pillar_construable(r, c, pillars, bos, n):
    """
    (r, c) 좌표에 기둥을 설치할 수 있는지 여부를 리턴한다.
    """
    if r == n:
        return True
    if pillars[r + 1][c]:
        return True
    if bos[r][c - 1] or bos[r][c]:
        return True

    return False


def is_pillar_deconstruable(r, c, pillars, bos, n):
    """
    (r, c) 좌표에 설치된 기둥을 제거할 수 있는지 여부를 리턴한다.
    """
    # 위에 있는 기둥 때문에 제거할 수 없는 경우
    if r > 1 and pillars[r - 1][c]:
        if not bos[r - 1][c - 1] and not bos[r - 1][c]:
            return False
    # 왼쪽 위에 있는 보 때문에 제거할 수 없는 경우
    if c > 0 and bos[r - 1][c - 1] and not pillars[r][c - 1]:
        if c < 2 or not (bos[r - 1][c - 2] and bos[r - 1][c]):
            return False
    # 오른쪽 위에 있는 보 때문에 제거할 수 없는 경우
    if c < n and bos[r - 1][c] and not pillars[r][c + 1]:
        if c < 1 or not (bos[r - 1][c - 1] and bos[r - 1][c + 1]):
            return False

    return True


def is_bo_constructable(r, c, pillars, bos, n):
    """
    (r, c) 좌표에 보를 설치할 수 있는지 여부를 리턴한다.
    """
    if pillars[r + 1][c] or pillars[r + 1][c + 1]:
        return True
    if 1 <= c < n - 1 and bos[r][c - 1] and bos[r][c + 1]:
        return True

    return False


def is_bo_deconstructable(r, c, pillars, bos, n):
    """
    (r, c) 좌표에 설치된 보를 제거거할 수 있는지 여부를 리턴한다.
    """
    # 왼쪽 위에 있는 기둥 때문에 제거할 수 없는 경우
    if pillars[r][c] and not pillars[r + 1][c]:
        if c == 0 or not bos[r][c - 1]:
            return False
    # 오른쪽 위에 있는 기둥 때문에 제거할 수 없는 경우
    if pillars[r][c + 1] and not pillars[r + 1][c + 1]:
        if c == n - 1 or not bos[r][c + 1]:
            return False
    # 왼쪽에 있는 보 때문에 제거할 수 없는 경우
    if c > 0 and bos[r][c - 1]:
        if not pillars[r + 1][c] and not pillars[r + 1][c - 1]:
            return False
    # 오른쪽에 있는 보 때문에 제거할 수 없는 경우
    if c < n - 1 and bos[r][c + 1]:
        if not pillars[r + 1][c + 1] and not pillars[r + 1][c + 2]:
            return False

    return True


def solution(n, build_frame):
    pillars = [[False] * (n + 1) for _ in range(n + 1)]
    bos = [[False] * (n + 1) for _ in range(n + 1)]

    for c, r, a, b in build_frame:
        r = n - r
        work = 2 * a + b

        if work == 0:    # 기둥 삭제
            if is_pillar_deconstruable(r, c, pillars, bos, n):
                pillars[r][c] = False
        elif work == 1:  # 기둥 설치
            if is_pillar_construable(r, c, pillars, bos, n):
                pillars[r][c] = True
        elif work == 2:  # 보 삭제
            if is_bo_deconstructable(r, c, pillars, bos, n):
                bos[r][c] = False
        else:            # 보 설치
            if is_bo_constructable(r, c, pillars, bos, n):
                bos[r][c] = True

    result = []

    for r in range(n + 1):
        for c in range(n + 1):
            if pillars[r][c]:
                result.append([c, n - r, 0])
            if bos[r][c]:
                result.append([c, n - r, 1])

    result.sort(key=lambda x: x[2])
    result.sort(key=lambda x: x[1])
    result.sort(key=lambda x: x[0])

    return result

print(solution(5, [[1,0,0,1],[1,1,1,1],[2,1,0,1],[2,2,1,1],[5,0,0,1],[5,1,0,1],[4,2,1,1],[3,2,1,1]]))
print(solution(5, [[0,0,0,1],[2,0,0,1],[4,0,0,1],[0,1,1,1],[1,1,1,1],[2,1,1,1],[3,1,1,1],[2,0,0,0],[1,1,1,0],[2,2,0,1]]))
