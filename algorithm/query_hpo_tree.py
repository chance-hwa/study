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