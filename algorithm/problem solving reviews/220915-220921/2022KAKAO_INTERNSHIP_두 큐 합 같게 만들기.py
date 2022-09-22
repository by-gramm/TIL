from collections import deque


def solution(queue1, queue2):
    left_sum = sum(queue1)
    right_sum = sum(queue2)
    NUM_COUNT = len(queue1) * 2

    queue1 = deque(queue1)
    queue2 = deque(queue2)

    if (left_sum + right_sum) % 2 == 1:
        return -1

    work_count = 0

    for _ in range(NUM_COUNT * 2):
        if left_sum == right_sum:
            return work_count

        if left_sum > right_sum:
            number = queue1.popleft()
            left_sum -= number

            queue2.append(number)
            right_sum += number
        else:
            number = queue2.popleft()
            right_sum -= number

            queue1.append(number)
            left_sum += number

        work_count += 1

    return -1
