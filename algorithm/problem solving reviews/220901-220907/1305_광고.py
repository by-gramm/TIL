from sys import stdin


L = int(stdin.readline())
board = stdin.readline().rstrip()
lps = [0] * L

length, idx = 0, 1

while idx < L:
    if board[length] == board[idx]:
        length += 1
        lps[idx] = length
        idx += 1
    else:
        if length:
            length = lps[length - 1]
        else:
            idx += 1

print(L - lps[-1])
