from sys import stdin


def get_lps(s, lps, s_len):
    length, idx = 0, 1

    while idx < s_len:
        if s[length] == s[idx]:
            length += 1
            lps[idx] = length
            idx += 1
        else:
            if length:
                length = lps[length - 1]
            else:
                idx += 1


while True:
    S = stdin.readline().rstrip()
    S_LEN = len(S)

    if S == '.':
        break

    lps = [0] * len(S)
    get_lps(S, lps, S_LEN)

    value, rest = divmod(S_LEN, S_LEN - lps[-1])

    if rest:
        print(1)
    else:
        print(value)
