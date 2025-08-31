"""
Human Phenotype Ontology(HPO) 트리는 각 노드가 증상을 나타내고, 증상들끼리 상하위 관계를 가지는 Tree 구조입니다.

이번 문제에서는 각 증상의 상위 증상은 유일하다고 가정합니다.

HPO tree 구조가 주어졌을 때, 여러 분은 여러 쌍의 증상(a, b)에 대해 아래와 같이 구분하고자 합니다.

a가 b의 조상(상위 증상)인지,

b가 a의 조상인지,

아니면 연관이 없는 증상인지 (위의 두 조건에 포함되지 않는 경우),

입력

hpo_trees (List[Tuple[int, int]]): HPO 트리를 구성하는 (부모, 자식) 쌍들의 리스트

queries (List[Tuple[int, int]]): 증상 구조를 확인하기 위한 (a, b) 쌍의 리스트

출력:

(List[str]): 주어진 쿼리 (a, b)에 대해

"ANCESTOR" (a가 b의 조상)

"DESCENDANT" (b가 a의 조상)

"NONE" (연관 없음)
중 하나를 출력하는 리스트


Input: 
hpo_trees = [
    (1, 2),
    (1, 3),
    (2, 4),
    (2, 5)
]
queries = [
    (1, 4),
    (4, 2),
    (5, 3),
    (2, 3)
]

Output:
[
    "ANCESTOR",
    "DESCENDANT",
    "NONE",
    "NONE"
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
    "ANCESTOR",
    "ANCESTOR",
    "ANCESTOR",
    "DESCENDANT",
    "DESCENDANT",
    "NONE",
    "DESCENDANT",
    "NONE",
    "NONE",
    "ANCESTOR"
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
from collections import defaultdict

def query_hpo_tree(hpo_trees, queries):
    tree = defaultdict(list)
    for parent, child in hpo_trees:
        tree[parent].append(child)

    def is_ancestor(a, b):
        for child in tree[a]:
            if child == b:
                return True
            if is_ancestor(child, b):
                return True
        return False
    
    result = list()
    for a, b in queries:
        if is_ancestor(a, b):
            result.append("ANCESTOR")
        elif is_ancestor(b, a):
            result.append("DESCENDANT")
        else:
            result.append("NONE")


    return result

hpo_trees = [
    (1, 2),
    (1, 3),
    (2, 4),
    (2, 5)
]
queries = [
    (1, 4),
    (4, 2),
    (5, 3),
    (2, 3)
]

print(query_hpo_tree(hpo_trees, queries))

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

print(query_hpo_tree(hpo_trees, queries))

"""
설명

이번 문제의 핵심은 DFS로 탐색해서 부모와 자식 노드를 판별하되, 쿼리가 여러 개인 경우를 푸는 것

 따라서 DFS로 탐색은 한 번만 하고 전처리를 통해 쿼리에는 O(1)의 시간복잡도를 가지도록 해야함

트리에서 a가 b의 조상인지 O(1)에 판단하려면, a의 서브트리 구간이 b의 구간을 완전히 포함하는지 확인

DFS로 방문할 때,

enter[x]는 x에 진입한 시점,

exit[x]는 x의 서브트리를 모두 순회하고 나오는 시점

따라서,

a가 b의 조상이면

enter[a] < enter[b] < exit[b] < exit[a]

반대로 b가 a의 조상인지도 같은 방식으로 체크

둘 다 아니라면 "NONE"

시간 복잡도: O(N + Q)

DFS 복잡도 O(N)

각 query 당 O(1)

전체 복잡도 = O(N + Q)

Q = len(query)

공간 복잡도: O(N)

enter, exit dict: O(N)
"""

from collections import defaultdict

def preprocess_hpo_tree(hpo_trees):
    tree = defaultdict(list)
    enter = dict()
    exit = dict()
    all_nodes = set()
    child_nodes = set()
    
    for parent, child in hpo_trees:
        tree[parent].append(child)
        all_nodes.add(parent)
        all_nodes.add(child)
        child_nodes.add(child)
        
    def dfs(u, index):
        enter[u] = index
        index += 1
        for v in tree[u]:
            index = dfs(v, index)
        exit[u] = index
        index += 1

        return index
        
    # root node가 하나라고 가정
    root = list(all_nodes - child_nodes)[0]
    dfs(root, 1)
    
    return enter, exit

def ancestor_query(enter, exit, a, b):
    if enter[a] < enter[b] and exit[b] < exit[a]:
        return "ANCESTOR"
    elif enter[b] < enter[a] and exit[a] < exit[b]:
        return "DESCENDANT"
    else:
        return "NONE"