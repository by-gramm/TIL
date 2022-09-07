from sys import stdin


def get_lps(target, lps, N):
    length, idx = 0, 1

    while idx < N:
        if target[length] == target[idx]:
            length += 1
            lps[idx] = length
            idx += 1
        else:
            if length:
                length = lps[length - 1]
            else:
                idx += 1


def get_count(target, board, lps, N):
    t_idx, b_idx = 0, 0
    count = 0

    while b_idx < 2 * N - 1:
        if target[t_idx] == board[b_idx]:
            t_idx += 1

            # 부분 문자열을 찾은 경우
            if t_idx == N:
                count += 1
                t_idx = lps[t_idx - 1]

            b_idx += 1
        else:
            if t_idx:
                t_idx = lps[t_idx - 1]
            else:
                b_idx += 1

    return count


def get_gcd(num1, num2):
    # num1 >= num2
    while num2:
        num1, num2 = num2, num1 % num2

    return num1


N = int(stdin.readline())
meat = stdin.readline().rstrip().replace(" ", "")
board = stdin.readline().rstrip().replace(" ", "")
board += board[:-1]

lps = [0] * N
get_lps(meat, lps, N)

count = get_count(meat, board, lps, N)
gcd = get_gcd(N, count)

print(str(count // gcd) + "/" + str(N // gcd))
