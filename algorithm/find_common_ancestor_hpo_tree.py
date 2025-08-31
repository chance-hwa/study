"""
Human Phenotype Ontology(HPO) 트리는 각 노드가 증상을 나타내고, 증상들끼리 상하위 관계를 가지는 Tree 구조입니다.

이번 문제에서는 각 증상의 상위 증상은 유일하다고 가정합니다.

HPO tree 구조가 주어졌을 때, 여러 분은 여러 쌍의 증상(a, b)에 대해 가장 가까운 공통 조상을 구하고자 합니다.

 

입력:

hpo_trees (List[Tuple[int, int]]): HPO 트리를 구성하는 (부모, 자식) 쌍들의 리스트

queries (List[Tuple[int, int]]): 가장 가까운 공통 조상을 확인하기 위한 (a, b) 쌍의 리스트

출력:

(List[int]): 주어진 (a, b) 쿼리에 대해 (a, b) 쌍의 최소공통조상 노드의 ID를 출력하는 리스트

Input: 
hpo_trees = [
    (1, 2),
    (1, 3),
    (2, 4),
    (2, 5)
]
queries = [
    (4, 5),
    (4, 3),
    (2, 3),
    (2, 5)
]

Output:
[
    2,
    1,
    1,
    2
]

Input: 
hpo_trees = [
    (1, 2),
    (1, 3),
    (2, 4),
    (2, 5),
    (3, 6),
    (3, 7),
    (5, 8),
    (5, 9),
    (6, 10),
    (6, 11),
    (11, 12)
]
queries = [
    (1, 12),
    (2, 8),
    (3, 11),
    (5, 1),
    (12, 6),
    (4, 8),
    (8, 5),
    (10, 12),
    (3, 5),
    (6, 12)
]

Output:
[
    1,
    2,
    3,
    1,
    6,
    2,
    5,
    6,
    1,
    6
]

Explanation:
1
├─ 2
│  ├─ 4
│  └─ 5
│      ├─ 8
│      └─ 9
└─ 3
    ├─ 6
    │   ├─ 10
    │   └─ 11
    │        └─ 12
    └─ 7
"""
"""
DFS with binary lifting
설명

쿼리가 여러 개이므로, tree 구조를 전처리하고, 쿼리에 드는 time complexity를 최소화 해야 합니다.

HPO tree를 처음 DFS로 탐색하면서

각 노드 u에 대해 2^0, 2^1, ..., 2^k번째 부모 노드를 미리 저장합니다.

쿼리 (a, b)마다

a, b의 깊이(depth)를 맞춘 뒤 동시에 2^k 단위로 부모를 올려보내며 처음으로 만나는 조상이 LCA가 됩니다.

핵심 원리:

쿼리 (a, b)의 깊이가 같다고 가정하면, a와 b의 조상 노드의 수는 같을 것이고, 이 조상노드를 맨 앞에서부터 부모까지 나열하면 “정렬”되었다고 할 수 있습니다.

따라서 조상노드들을 “binary search”처럼 찾으면서, 가장 “나중에” “같아지는” 노드가 최소공통조상입니다.

ex:

a: [1, 2, 3, 4, 7, 15, 23, 56]

b: [1, 2, 3, 4, 8, 25, 64, 82]

최소공통조상은 4

가장 오른쪽에서 같아지는 노드를 찾는 것이 아닌, 절반씩 search

전처리

트리 DFS로 각 노드의 부모(parent), 깊이(depth)를 기록합니다.

Binary Lifting 테이블(jump pointer table)을 채웁니다.

테이블을 채우는 방식은 DP를 이용합니다.

parents[u][k] = 노드 u의 2^k 번째 부모

점화식: parents[u][k] = parents[parents[u][k-1]][k-1]

노드 u의 2^k번째 부모는 u의 2^(k-1)번째 부모의 2^(k-1)번째 부모와 같다

쿼리 처리

두 노드의 깊이를 맞추고, logN번 점프하며 동시에 위로 올려서
최초로 만나는(같아지는) 노드를 반환합니다.


시간 복잡도: O(N * log D) + O(log D)
- 전처리: O(N * log D)
- 쿼리 질의: O(log D)
- N: 노드 수, D: 최대 depth

공간 복잡도: O(N * log D)
- parents 저장 크기

"""

from collections import defaultdict
import math

def preprocess_lca(hpo_trees):
    tree = defaultdict(list)
    all_nodes = set()
    child_nodes = set()
    
    for parent, child in hpo_trees:
        tree[parent].append(child)
        all_nodes.add(parent)
        all_nodes.add(child)
        child_nodes.add(child)
        
    root = list(all_nodes - child_nodes)[0]

    depth = {}
    jump = {}

    def dfs(u, parent, d):
        depth[u] = d
        jump[u] = [parent]
        max_sub_depth = d
        for v in tree[u]:
            child_max = dfs(v, u, d+1)
            max_sub_depth = max(max_sub_depth, child_max)
        return max_sub_depth

    max_depth = dfs(root, None, 0)

    LOG = math.ceil(math.log2(max_depth + 1))
    for u in all_nodes:
        parents[u] += [None]*LOG

    for k in range(1, LOG+1):
        for u in all_nodes:
            prev = parents[u][k-1]
            parents[u][k] = parents[prev][k-1] if prev is not None else None

    return depth, parents

def lca(a, b, depth, parents):
    if depth[a] < depth[b]:
        a, b = b, a
    LOG = len(parents[a]) - 1
    
    for k in range(LOG, -1, -1):
        if parents[a][k] is not None and depth[parents[a][k]] >= depth[b]:
            a = parents[a][k]
    if a == b:
        return a
    for k in range(LOG, -1, -1):
        if parents[a][k] != parents[b][k]:
            if parents[a][k] is not None and parents[b][k] is not None:
                a = parents[a][k]
                b = parents[b][k]
    return parents[a][0]