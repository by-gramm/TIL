from sys import stdin


def change_node(left, right, in_degrees, adj_list):
    adj_list[left].remove(right)
    adj_list[right].add(left)
    in_degrees[right] -= 1
    in_degrees[left] += 1


def get_order(N, numbers, changes):
    in_degrees = [0] * (N + 1)
    adj_list = [set() for _ in range(N + 1)]
    orders = []

    for idx, number in enumerate(numbers):
        in_degrees[number] = idx
        adj_list[number] = set(numbers[idx + 1:])

    for node1, node2 in changes:
        # node1이 node2의 선행 노드였던 경우
        if node2 in adj_list[node1]:
            change_node(node1, node2, in_degrees, adj_list)
        # node2가 node1의 선행 노드였던 경우
        else:
            change_node(node2, node1, in_degrees, adj_list)

    current = -1

    # 진입 차수가 0인 노드들을 찾는다.
    for idx in range(1, N + 1):
        if not in_degrees[idx]:
            if current != -1:
                return '?'
            current = idx

    if current == -1:
        return 'IMPOSSIBLE'

    for _ in range(N - 1):
        orders.append(current)
        before, current = current, -1

        for node in adj_list[before]:
            in_degrees[node] -= 1

            if not in_degrees[node]:
                if current != -1:
                    return '?'
                current = node

        if current == -1:
            return 'IMPOSSIBLE'

    orders.append(current)

    return " ".join([str(x) for x in orders])


T = int(stdin.readline())

for _ in range(T):
    n = int(stdin.readline())
    numbers = [int(x) for x in stdin.readline().split()]
    m = int(stdin.readline())
    changes = []

    for _ in range(m):
        a, b = map(int, stdin.readline().split())
        changes.append([a, b])

    print(get_order(n, numbers, changes))
