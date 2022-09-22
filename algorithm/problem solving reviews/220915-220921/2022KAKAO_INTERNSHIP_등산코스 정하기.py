from heapq import heappush, heappop
from math import inf


def solution(n, paths, gates, summits):
    gates_set = set(gates)

    distances = [inf] * (n + 1)
    adj_list = dict()

    for idx in range(1, n + 1):
        adj_list[idx] = dict()

    for i, j, w in paths:
        adj_list[i][j] = w
        adj_list[j][i] = w

    heap = []

    for summit in summits:
        heappush(heap, [0, summit, summit])

    while heap:
        cnt_intensity, summit, cnt_node = heappop(heap)

        if distances[cnt_node] <= cnt_intensity:
            continue

        distances[cnt_node] = cnt_intensity
        
        # 출입구를 방문한 경우
        if cnt_node in gates_set:
            return [summit, cnt_intensity]

        for node, distance in adj_list[cnt_node].items():
            intensity = max(cnt_intensity, distance)
            
            if distances[node] <= intensity:
                continue
            
            heappush(heap, [intensity, summit, node])
