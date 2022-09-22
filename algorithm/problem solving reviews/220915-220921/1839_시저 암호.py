"""
시간 초과
"""
from sys import stdin


def get_lps(lps, pattern):
    length, idx = 0, 1

    while idx < len(pattern):
        if pattern[idx] == pattern[length]:
            length += 1
            lps[idx] = length
            idx += 1
        else:
            if length:
                length = lps[length - 1]
            else:
                idx += 1


N = int(stdin.readline())

for _ in range(N):
    A = stdin.readline().rstrip()
    W = stdin.readline().rstrip()
    S = stdin.readline().rstrip()

    A_LEN, W_LEN, S_LEN = len(A), len(W), len(S)
    shifts = []

    lps = [0] * W_LEN
    get_lps(lps, W)

    for shift in range(A_LEN):
        # 각각의 시프트에 대하여 kmp로 탐색한다.
        # 부분 문자열이 하나만 존재하면 완료!
        w_idx, s_idx = 0, 0
        isShift = False

        while s_idx < S_LEN:
            if W[(w_idx + shift) % W_LEN] == S[s_idx]:
                w_idx += 1

                if w_idx == W_LEN:    # 부분 문자열 발견
                    if isShift:       # 부분 문자열이 2개 이상 => 탐색 종료
                        isShift = False
                        break
                    isShift = True
                    w_idx = lps[w_idx - 1]

                s_idx += 1
            else:
                if w_idx:
                    w_idx = lps[w_idx]
                else:
                    s_idx += 1

        if isShift:
            shifts.append(shift)

    if not shifts:
        print("no solution")
    if len(shifts) == 1:
        print("unique: " + str(shifts[0]))
    if len(shifts) >= 2:
        print("ambiguous: " + " ".join([str(x) for x in shifts]))
