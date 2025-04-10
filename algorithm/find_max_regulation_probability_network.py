"""
세포 내에서 유전자들은 특정 조절 네트워크를 통해 서로 영향을 미칠 수 있습니다. 일부 유전자는 다른 유전자의 발현을 촉진하거나 억제할 수 있습니다.

예를 들어, 유전자 A가 유전자 B를 조절하고, 유전자 B가 유전자 C를 조절하지만, 유전자 C는 유전자 A를 직접 조절하지 않을 수도 있습니다.

각 유전자가 어떤 유전자를 조절할 확률들이 주어졌을 때, 어떤 유전자 X가 다른 유전자 Y를 조절할 최대 확률을 구해보세요.

입력:

regulation_network (2D list, n x n): 유전자 조절 관계를 나타내는 데이터.

0 ≤ regulation_network[i][j] ≤ 1

항상 regulation_network[i][j] == regulation[j][i] 인 것은 아님 (방향성이 있음)

regulation_network[i][j] = 유전자 i가 유전자 j를 조절할 확률

항상 regulation_network[i][i] = 1 

x (int): 조절 네트워크에서 조절을 시작하는 유전자의 index

0 ≤ x < n

y (int): 조절 네트워크에서 조절 될 확률을 구하고 싶은 유전자의 index

0 ≤ y < n

출력:

(float): 유전자 x가 유전자 y를 조절할 최대 확률

조절이 불가능하다면 0

예제 1:
Input: 
regulation_network = [
  [1, 0.5, 0.2],
  [0.5, 1, 0.5],
  [0.2, 0.5, 1]
]
x = 0
y = 2

Output:
0.25

Explanation:
0 -> 1 -> 2 순으로 조절했을 때 0.5 * 0.5 = 0.25로 최대의 확률


예제 2:
Input: 
regulation_network = [
    [1, 0.8, 0.0, 0.0],
    [0.0, 1, 0.5, 0.6],
    [0.0, 0.0, 1, 0.7],
    [0.2, 0.0, 0.0, 1]
]
x = 0
y = 3

Output:
0.48

Explanation:
0 -> 1 -> 3 순으로 조절했을 때 0.8 * 0.6 = 0.48로 최대의 확률
0 -> 1 -> 2 -> 3 순으로 조절한다면 0.8 * 0.5 * 0.7 = 0.28
"""
from itertools import permutations

def find_max_regulation_probability_brute(regulation_network, x, y):
    n = len(regulation_network)
    max_prob = 0.0

    all_network_order = list(permutations(range(n)))
    for network_order in all_network_order:
        x_index = network_order.index(x)
        y_index = network_order.index(y)
        if x_index < y_index:
            prob = 1.0
            for i in range(x_index, y_index):
                prob *= regulation_network[network_order[i]][network_order[i+1]]
            max_prob = max(max_prob, prob)
    
    return max_prob
        
# Test
regulation_network = [
    [1, 0.5, 0.2],
    [0.5, 1, 0.5],
    [0.2, 0.5, 1]
]
x = 0
y = 2
print(find_max_regulation_probability_brute(regulation_network, x, y))

regulation_network = [
    [1, 0.8, 0.0, 0.0],
    [0.0, 1, 0.5, 0.6],
    [0.0, 0.0, 1, 0.7],
    [0.2, 0.0, 0.0, 1]
]
x = 0
y = 3
print(find_max_regulation_probability_brute(regulation_network, x, y))


"""
brute force: 
dfs에 방문한 사실을 초기화 시켜주면 모든 경로를 탐색 가능함. 거기서 최댓값을 고르면 됨.
time complexity O(2^n) 노드의 갯수 n개, 노드를 쓰느냐 안쓰느냐

다익스트라 알고리즘으로 풀 수 있음.
최단 경로를 구할 때 가장 많이 쓰는 알고리즘 중 하나.
경로는 덧셈이니까 inf로 초기화, 작은 값으로 대체,
확률에서는 곱셈이니까 0으로 초기화, 큰 값으로 대체
min, max 구하는게 비효율적이라 heap이라는 자료구조를 쓰게 됨.
time complexity O((n+E)*log(n)) E는 edge의 갯수, heap에 n개의 노드 들어감

bfs로 풀되, 거리를 갱신. 
"""

def max_prob_dfs(regulation_network, x, y):
    n = len(regulation_network)
    visited = [False] * n
    max_prob = 0.0

    def dfs(node, prob):
        nonlocal max_prob
        if node == y:
            max_prob = max(max_prob, prob)
            return
        visited[node] = True
        for neighbor in range(n):
            if not visited[neighbor] and regulation_network[node][neighbor] > 0:
                dfs(neighbor, prob * regulation_network[node][neighbor])
        visited[node] = False

    dfs(x, 1.0)
    return max_prob

import heapq

def max_prob_dijkstra(regulation_network, x, y):
    n = len(regulation_network)
    probs = [0.0] * n
    probs[x] = 1.0
    max_heap = [(-1.0, x)]  # (음수 확률, 노드 번호)

    while max_heap:
        neg_prob, node = heapq.heappop(max_heap)
        prob = -neg_prob

        # 목적지에 도달하면 바로 종료
        if node == y:
            return prob

        # 이미 더 높은 확률로 방문된 경우는 무시
        if prob < probs[node]:
            continue

        for neighbor in range(n):
            if neighbor == node or regulation_network[node][neighbor] == 0:
                continue
            new_prob = prob * regulation_network[node][neighbor]
            if new_prob > probs[neighbor]:
                probs[neighbor] = new_prob
                heapq.heappush(max_heap, (-new_prob, neighbor))

    # 도달할 수 없는 경우
    return 0.0