"""
문제
당신은 유전체 분석 파이프라인을 구성한 뒤, 모든 분석 단계(sequence)와 실행 순서를 정의한 선행 조건(dependency)을 잘 설정해두었습니다.
하지만 실수로 분석 단계들의 순서가 뒤섞인 채로 Git repository에 push해버렸습니다.

섞인 상태의 분석 단계 리스트와 선행 조건 정보를 바탕으로, 파이프라인이 정상적으로 실행 가능한 순서로 복구되도록 정렬하세요. 

단, 만약 의존성 조건에 따라 정상적으로 실행 가능한 순서로 복구가 불가능하다면, 빈 리스트를 출력하세요.

입력:

sequence (List[str]): 분석 단계들의 이름이 섞인 리스트 (모든 분석의 이름은 유니크함)

dependency: Dict[str, List[str]]: 각 분석 단계가 실행되기 위해 필요한 선행 단계들의 이름

dependency에 명시되지 않은 분석은 선행 조건이 없는 것으로 간주

출력:

(List[str]): 의존성 조건에 모두 만족하는 실행 가능한 분석들의 정렬된 리스트

복구가 불가능하다면, 빈 리스트를 출력하세요.

여러가지 케이스가 가능하다면, 그 중 하나만 출력해도 됩니다.

예제 1:
Input: 
sequence = ["EXPANSION_HUNTER", "BWA_GATK", "PHASING_STAT_EXTRACTOR", "EVI_PREP-PROBAND"]
dependency = {
    "EXPANSION_HUNTER": ["BWA_GATK"],
    "PHASING_STAT_EXTRACTOR": ["BWA_GATK"],
    "EVI_PREP-PROBAND": ["EXPANSION_HUNTER", "PHASING_STAT_EXTRACTOR"]
}

Output:
["BWA_GATK", "PHASING_STAT_EXTRACTOR", "EXPANSION_HUNTER", "EVI_PREP-PROBAND"]

Explanation:
다른 순서도 가능(EXPANSION_HUNTER와 PHASING_STAT_EXTRACTOR의 순서가 바뀌어도 됨)

예제 2:
Input: 
sequence = ["A", "B", "C"]
dependency = {
    "A": ["B"],
    "B": ["C"],
    "C": ["A"]
}

Output:
[]

Explanation:
어떤 순서로도 정상적으로 분석 파이프라인을 구성할 수 없음 (서로 순환된 구조)

예제 3:
Input: 
sequence = ["F", "C", "A", "J", "B", "I", "H", "E", "G", "D"]
dependency = {
    "B": ["A"],
    "C": ["B"],
    "D": ["C"],
    "E": ["D"],
    "F": ["C"],
    "G": ["E", "F"],
    "H": ["G"],
    "I": ["H"],
    "J": ["I"]
}

Output:
["A", "B", "C", "D", "F", "E", "G", "H", "I", "J"]

Explanation:
다른 순서도 가능
"""

from itertools import permutations

def recover_analysis_pipeline(sequence, dependency):
    all_sequences_permutations = list(permutations(sequence))

    for sequence in all_sequences_permutations:
        seq_dict = {seq: idx for idx, seq in enumerate(sequence)}

        is_valid = True
        for seq, deps in dependency.items():
            for dep in deps:
                if seq_dict[seq] < seq_dict[dep]:
                    is_valid = False
                    break

        if is_valid:
            return list(sequence)
    
    return list()
    

sequence = ["EXPANSION_HUNTER", "BWA_GATK", "PHASING_STAT_EXTRACTOR", "EVI_PREP-PROBAND"]
dependency = {
    "EXPANSION_HUNTER": ["BWA_GATK"],
    "PHASING_STAT_EXTRACTOR": ["BWA_GATK"],
    "EVI_PREP-PROBAND": ["EXPANSION_HUNTER", "PHASING_STAT_EXTRACTOR"]
}

print(recover_analysis_pipeline(sequence, dependency))

sequence = ["A", "B", "C"]
dependency = {
    "A": ["B"],
    "B": ["C"],
    "C": ["A"]
}

print(recover_analysis_pipeline(sequence, dependency))

sequence = ["F", "C", "A", "J", "B", "I", "H", "E", "G", "D"]
dependency = {
    "B": ["A"],
    "C": ["B"],
    "D": ["C"],
    "E": ["D"],
    "F": ["C"],
    "G": ["E", "F"],
    "H": ["G"],
    "I": ["H"],
    "J": ["I"]
}

print(recover_analysis_pipeline(sequence, dependency))


"""
설명

각 노드를 DFS로 방문하면서,

방문한 노드는 방문 중으로 표시

모든 노드를 방문하고 나갈 때는 방문 완료로 표시

방문한 노드가 방문 중이면 사이클

방문 완료인 노드는 스킵

종료된 순서대로 stack에 push (역순으로 topological order 생성)
"""
from typing import List, Dict
from collections import defaultdict

def recover_pipeline_order_dfs(sequence: List[str], dependency: Dict[str, List[str]]) -> List[str]:
    graph = defaultdict(list)
    visited = set()     # 탐색 완료한 노드
    visiting = set()    # 탐색 중인 노드
    result = []

    # 그래프 구성
    for u in dependency:
        for v in dependency[u]:
            graph[v].append(u)

    def dfs(node: str) -> bool:
        if node in visiting:
            return False  # 사이클 발견
        if node in visited:
            return True   # 방문을 완료한 노드

        visiting.add(node)
        for neighbor in graph[node]:
            if not dfs(neighbor):
                return False
        visiting.remove(node)
        visited.add(node)
        result.append(node)
        return True

    for node in sequence:
        if node not in visited:
            if not dfs(node):
                return []  # 사이클 → 복구 불가

    return result[::-1]  # 후위 순회 결과 뒤집기

"""
시간 복잡도: O(N + M)

노드 수 N / 엣지 수 M

그래프 구성 O(N+M) / 탐색 O(N + M)

공간 복잡도: O(N)

재귀 복잡도 N

visiting, visted, result 크기 N
"""

"""
설명

그래프에서 진입 차수(in-degree)를 계산

in-degree가 0인 노드부터 큐에 넣어 정렬 순서를 만들고, 그 노드가 연결된 노드들의 in-degree를 줄인다

줄인 in-degree가 0이면 다시 큐에 삽입

위상 정렬한 노드 개수 < 전체 노드 수 → 사이클 존재
"""
from collections import deque

def recover_pipeline_order_kahn(sequence: List[str], dependency: Dict[str, List[str]]) -> List[str]:
    graph = defaultdict(list)
    in_degree = {node: 0 for node in sequence}

    # 그래프 구성
    for u in dependency:
        for v in dependency[u]:  # v → u
            graph[v].append(u)
            in_degree[u] += 1

    # dependency가 없는 분석(노드)들로 초기화
    queue = deque([node for node in sequence if in_degree[node] == 0])
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return result if len(result) == len(sequence) else []

"""
시간 복잡도: O(N+M)

그래프 구성 O(N+M) / 탐색 O(N+M)

공간 복잡도: O(N)

graph, in_degree, queue 크기 N
"""