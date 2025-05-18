"""
문제
어떤 환자의 증상 정보를 가지고 있고, 유전자 별로 그 유전자가 설명할 수 있는 증상 정보도 가지고 있다고 가정해보세요.

주어진 환자의 증상 정보를 모두 설명할 수 있는 유전자들의 조합 중 최소의 유전자 개수를 가지는 조합을 구해보세요.

입력:

symptoms (List[int]): 분석 대상 증상의 번호 리스트

1 <= len(symptoms) <= 16

genes (List[List[int]]): genes[i]는 i번째 유전자가 유발하는 증상 번호 리스트

1 <= len(genes) <= 60

출력:

(List[int]): 모든 증상을 커버할 수 있는 최소 유전자 인덱스들의 리스트

여러 정답이 있을 수 있으며, 유전자의 개수만 같다면 어느 것이든 정답

예제 1:
Input: 
symptoms = [0, 1, 2]
genes = [
    [0],
    [1],
    [2],
    [0, 2]
]

Output:
[1, 3]

Explanation:
genes[1]과 genes[3] 만으로 증상 정보 설명 가능

예제 2:
Input: 
symptoms = [0, 1, 2, 3]
genes = [
    [0, 1],
    [2, 3],
    [0, 1, 2, 3]
]

Output:
[2]

Explanation:
genes[2]만으로 증상 정보 설명 가능

예제 3:
Input: 
symptoms = [0, 1, 2, 3, 4]
genes = [
    [0, 2],
    [1, 3],
    [4],
    [0, 1],
    [2, 4]
]

Output:
[0, 1, 2] 또는 [1, 3, 4]

Explanation:
최소 3개의 유전자로만 설명 가능
"""

from itertools import combinations

def get_least_explainable_genes(symptoms, genes):
    gene_number = 1
    while gene_number <= len(genes):
        for gene_combination in combinations(range(1,len(genes)), gene_number):
            explainable_symptoms = set()
            for gene in gene_combination:
                explainable_symptoms.update(genes[gene])
            if explainable_symptoms == set(symptoms):
                return list(gene_combination)
        gene_number += 1

    return "Not Explanable"

symptoms = [0, 1, 2]
genes = [[0],[1],[2],[0, 2]]
print(get_least_explainable_genes(symptoms, genes))

symptoms = [0, 1, 2, 3]
genes = [
    [0, 1],
    [2, 3],
    [0, 1, 2, 3]
]
print(get_least_explainable_genes(symptoms, genes))

symptoms = [0, 1, 2, 3, 4]
genes = [
    [0, 2],
    [1, 3],
    [4],
    [0, 1],
    [2, 4]
]
print(get_least_explainable_genes(symptoms, genes))


"""
brute force
genes 개수(m), symptoms 개수(n) 2^m * n 만큼 연산
greedy n * m 에다가 set 비교만큼 연산 추가
dp로 풀 수 있을까? -> dp[지금 커버하는 증상] = min(dp[지금 커버하는 증상], dp[이전에 커버한 증상 + 지금 gene의 증상] + 1)
증상을 가지고 있다는 bit (bit masking)
bit로 하면 O(1)로 증상 커버 여부 확인 가능
따라서 time complexity는 O(2^n)
"""

"""
Brute Force

가능한 유전자 조합 (부분집합) 2^n개를 모두 확인

각 조합이 모든 필수 증상을 커버하는지 검사

커버하는 조합 중 유전자 수가 가장 적은 것을 선택

시간 복잡도: O(2^n * m)

n = 유전자 수, m = 증상 수

공간 복잡도: O(n + m)

재귀 깊이 n, 현재 커버하는 유전자 저장 m
"""

def min_genes_brute_force_recursive(required_symptoms, genes):
    symptom_set = set(required_symptoms)
    n = len(genes)
    min_gene_count = [float('inf')]

    def backtrack(index, selected_genes, covered_symptoms):
        if symptom_set.issubset(covered_symptoms):
            min_gene_count[0] = min(min_gene_count[0], len(selected_genes))
            return

        if index == n or len(selected_genes) >= min_gene_count[0]:
            return

        # 선택하지 않는 경우
        backtrack(index + 1, selected_genes, covered_symptoms)

        # 선택하는 경우
        next_covered = covered_symptoms.union(genes[index])
        backtrack(index + 1, selected_genes + [index], next_covered)

    backtrack(0, [], set())

    return min_gene_count[0] if min_gene_count[0] != float('inf') else -1

"""
Bitmask + DP

각 증상 집합을 bitmask로 표현

dp[mask]: 증상 상태가 mask일 때 필요한 최소 유전자 수

초기 상태: dp[0] = 0

각 유전자의 증상 → bitmask로 변환해서 dp 갱신

점화식
for gene in genes:
    gene_mask = bitmask of gene’s symptoms
    for prev_mask in dp:
        new_mask = prev_mask | gene_mask
        dp[new_mask] = min(dp[new_mask], dp[prev_mask] + 1)

시간 복잡도: O(n * 2^m)
n = 유전자 수, m = 증상 수

공간 복잡도: O(2^m)
dp 크기 2^m
"""

def min_genes_bitmask_dp(required_symptoms, genes):
    symptom_to_bit = {s: i for i, s in enumerate(required_symptoms)}
    total = (1 << len(required_symptoms)) - 1
    dp = {0: 0}

    for gene in genes:
        mask = 0
        for s in gene:
            if s in symptom_to_bit:
                mask |= 1 << symptom_to_bit[s]

        if mask == 0:
            continue

        new_dp = dict(dp)
        for prev_mask, cnt in dp.items():
            combined = prev_mask | mask
            if combined not in new_dp or new_dp[combined] > cnt + 1:
                new_dp[combined] = cnt + 1
        dp = new_dp

    return dp.get(total, -1)