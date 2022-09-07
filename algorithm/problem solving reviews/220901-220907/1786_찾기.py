from sys import stdin


def compute_lps(pattern, lps):
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
                lps[idx] = 0
                idx += 1


def kmp_search(pattern, text):
    """
    kmp 알고리즘을 이용하여 text 내에 pattern의 개수 및 인덱스를 구한다.
    """
    N, M = len(text), len(pattern)
    lps = [0] * M
    compute_lps(pattern, lps)

    p_idx, t_idx = 0, 0
    count = 0
    start_index_list = []

    while t_idx < N:
        if pattern[p_idx] == text[t_idx]:
            # 부분 문자열을 발견한 경우
            if p_idx == M - 1:
                count += 1
                start_index_list.append(t_idx - M + 2)  # 문자열은 1번부터 시작
                p_idx = lps[p_idx]
            else:
                p_idx += 1

            t_idx += 1
        else:
            if p_idx:
                p_idx = lps[p_idx - 1]
            else:
                t_idx += 1

    print(count)

    for start_idx in start_index_list:
        print(start_idx, end=" ")


T = stdin.readline().rstrip()
P = stdin.readline().rstrip()
kmp_search(P, T)
