'''
문제
세포 내에서 유전자들은 특정 조절 네트워크를 통해 서로 영향을 미칠 수 있습니다. 일부 유전자는 다른 유전자의 발현을 촉진하거나 억제할 수 있습니다.

예를 들어, 유전자 A가 유전자 B를 조절하고, 유전자 B가 유전자 C를 조절하지만, 유전자 C는 유전자 A를 직접 조절하지 않을 수도 있습니다.

각 유전자 간의 조절 관계가 주어졌을 때, 독립적인 유전자 조절 그룹의 개수를 찾으세요.

입력:

regulation_network (2D list, n x n): 유전자 조절 관계를 나타내는 데이터.

regulation_network[i][j] = 1이면 유전자 i가 유전자 j의 발현을 조절함.

regulation_network[i][j] = 0이면 유전자 i가 유전자 j를 조절하지 않음.

항상 regulation_network[i][i] = 1 (유전자는 자기 자신을 조절 가능).

출력:

(int): 독립적인 유전자 조절 그룹(Clusters)의 개수.

'''
from collections import defaultdict

def find_gene_groups(regulation_network):
    gene2regulators = defaultdict(set)
    for i in range(len(regulation_network)):
        for j in range(len(regulation_network)):
            if regulation_network[i][j] == 1:
                gene2regulators[i].add(j)
    
    clusters = list()
    for gene in gene2regulators:
        regulators = gene2regulators[gene]
        if not clusters:
            clusters.append(regulators)
        else:
            for cluster in clusters:
                if cluster & regulators:
                    cluster.update(regulators)
                    break
            else:
                clusters.append(regulators)
    
    return len(clusters)
        

#Example test cases
regulation_network = [
    [1,1,0],  
    [0,1,1],  
    [0,0,1]
]
print(find_gene_groups(regulation_network))
# 1

regulation_network = [
    [1,0,0],  
    [0,1,1],  
    [0,0,1]
]
print(find_gene_groups(regulation_network))
# 2

regulation_network = [
    [1,0,0,0],
    [0,1,1,0],
    [1,0,1,0],
    [0,0,1,1]
]
print(find_gene_groups(regulation_network))
# 2, wrong answer

"""
예제 1:

Input:
regulation_network = [
    [1,1,0],  
    [0,1,1],  
    [0,0,1]
]

Output:
1
유전자 0은 유전자 1을 조절하고, 유전자1은 유전자 2를 조절하므로 크게 1 개의 그룹을 형성함

예제 2:

Input:
regulation_network = [
    [1,0,0],  
    [0,1,1],  
    [0,0,1]
]

Output:
2
유전자 0은 독립적으로 존재하고, 유전자 1은 유전자 2를 조절하는 그룹 1개가 존재하므로 크게 2개의 그룹을 형성함
"""


"""
위 풀이는 한쪽에만 관계가 있을 시 정답을 도출하며 대각선 반대편에 있으면 오답이 나오게 됨.

알고리즘을 BFS (너비 우선 탐색) 와 DFS (깊이 우선 탐색) 로 풀 수 있음.
DFS로 풀면 visited를 사용하여 방문한 노드를 체크하고, 방문하지 않은 노드를 탐색하며 그룹을 형성하게 됨.
이 문제 한정 union find를 사용하여 풀 수 있음. clustering에 특화되어 있음.
"""

def count_regulatory_clusters_dfs(regulation_network):
    n = len(regulation_network)
    visited = [False] * n
    num_clusters = 0  

    def dfs(node):
        for neighbor in range(n):
            if not visited[neighbor] and (regulation_network[node][neighbor] == 1 or regulation_network[neighbor][node] == 1):
                visited[neighbor] = True
                dfs(neighbor)

    for i in range(n):
        if not visited[i]:  # 새로운 조절 그룹 발견
            visited[i] = True
            dfs(i)
            num_clusters += 1  

    return num_clusters

#Example test cases
regulation_network = [
    [1,1,0],  
    [0,1,1],  
    [0,0,1]
]
print(count_regulatory_clusters_dfs(regulation_network))
# 1

regulation_network = [
    [1,0,0],  
    [0,1,1],  
    [0,0,1]
]
print(count_regulatory_clusters_dfs(regulation_network))
# 2

regulation_network = [
    [1,0,0,0],
    [0,1,1,0],
    [1,0,1,0],
    [0,0,1,1]
]
print(count_regulatory_clusters_dfs(regulation_network))
# 1

from collections import deque

def count_regulatory_clusters_bfs(regulation_network):
    n = len(regulation_network)
    visited = [False] * n
    num_clusters = 0  

    for i in range(n):
        if not visited[i]:  # 새로운 조절 그룹 발견
            queue = deque([i])
            visited[i] = True
            while queue:
                node = queue.popleft()
                for neighbor in range(n):
                    if not visited[neighbor] and (regulation_network[node][neighbor] == 1 or regulation_network[neighbor][node] == 1):
                        visited[neighbor] = True
                        queue.append(neighbor)
            num_clusters += 1  

    return num_clusters


## Union-Find
# 기본적인 Union-Find 구현
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, x):
        if self.parent[x] == x:
            return x
        return self.find(self.parent[x])  # 경로 압축 없음

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            self.parent[root_y] = root_x  # 두 그룹을 하나로 합침

# 최적화된 Union-Find 구현
class OptimizedUnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [1] * n  # 각 노드의 트리 높이(랭크)

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # 경로 압축 적용
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x != root_y:
            if self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            elif self.rank[root_x] < self.rank[root_y]:
                self.parent[root_x] = root_y
            else:
                self.parent[root_y] = root_x
                self.rank[root_x] += 1
  
def count_regulatory_clusters_union_find(regulation_network):
    n = len(regulation_network)
    uf = OptimizedUnionFind(n)

    for i in range(n):
        for j in range(i + 1, n):
            if regulation_network[i][j] == 1 or regulation_network[j][i] == 1:
                uf.union(i, j)

    return len(set(uf.find(i) for i in range(n)))
