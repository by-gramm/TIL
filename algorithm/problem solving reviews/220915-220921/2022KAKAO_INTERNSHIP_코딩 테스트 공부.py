def solution(alp, cop, problems):
    filtered_problems = []
    A, C = 0, 0

    for alp_req, cop_req, alp_rwd, cop_rwd, cost in problems:
        A = max(A, alp_req)
        C = max(C, cop_req)

        if alp_rwd + cop_rwd > cost:
            alp_left = max(0, alp_req - alp)
            cop_left = max(0, cop_req - cop)
            filtered_problems.append([alp_left, cop_left, alp_rwd, cop_rwd, cost])

    A = max(0, A - alp)
    C = max(0, C - cop)
    min_costs = [[0] * (C + 1) for _ in range(A + 1)]

    for r in range(A + 1):
        for c in range(C + 1):
            min_costs[r][c] = r + c

    for r in range(A + 1):
        for c in range(C + 1):
            if r != A:
                min_costs[r + 1][c] = min(min_costs[r + 1][c], min_costs[r][c] + 1)
            if c != C:
                min_costs[r][c + 1] = min(min_costs[r][c + 1], min_costs[r][c] + 1)

            for alp_req, cop_req, alp_rwd, cop_rwd, cost in filtered_problems:
                if r >= alp_req and c >= cop_req and min_costs[r][c] + cost < min_costs[A][C]:
                    nr = min(r + alp_rwd, A)
                    nc = min(c + cop_rwd, C)
                    min_costs[nr][nc] = min(min_costs[nr][nc], min_costs[r][c] + cost)

    return min_costs[A][C]
