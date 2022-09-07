from sys import stdin
from collections import deque


N, M = map(int, stdin.readline().split())
adj_list = [set() for _ in range(N + 1)]
ingredients = [[] for _ in range(N + 1)]

for _ in range(M):
    k, *recipes, r = [int(x) for x in stdin.readline().split()]

    for recipe in recipes:
        adj_list[recipe].add(r)

    ingredients[r].append(set(recipes))

L = int(stdin.readline())
potions = [int(x) for x in stdin.readline().split()]
makeable = [False] * (N + 1)
queue = deque()

for potion in potions:
    makeable[potion] = True
    queue.append(potion)

while queue:
    current = queue.popleft()

    for potion in adj_list[current]:
        if not makeable[potion]:
            for recipe_set in ingredients[potion]:
                if current in recipe_set:
                    recipe_set.remove(current)

                    if not recipe_set:
                        makeable[potion] = True
                        queue.append(potion)
                        break

result = []

for idx in range(1, N + 1):
    if makeable[idx]:
        result.append(idx)

print(len(result))
print(" ".join([str(x) for x in result]))
