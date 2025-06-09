'''
start, end, impact_score로 표현되는 유전자 클러스터(변이 집합)가 있다고 가정합니다. 
이 클러스터들 중에서 서로 겹치지 않는 클러스터들을 골라 총 impact_score가 최대가 되도록 선택해보세요.

모든 클러스터 구간은 [start, end)로 정의되며, 즉 start ≤ position < end 범위에 해당하는 염기서열을 포함합니다.

클러스터 구간은 정렬되지 않았을 수도 있습니다.

두 클러스터가 단 하나의 base라도 겹치면 함께 선택할 수 없습니다.

입력:
clusters(list):  [start: int, end: int, impact_score: int]로 표현되는 클러스터들의 리스트

출력:
(int): 선택 가능한 비중복 클러스터들의 최대 impact_score의 합

Input: 
clusters = [
    [0, 10, 3],
    [10, 20, 5],
    [20, 30, 2],
]

Output:
10
Explanation:
서로 겹치지 않으므로 모두 선택 가능. 총 합 = 3 + 5 + 2 = 10

Input: 
clusters = [
    [0, 10, 3],
    [9, 20, 5],
    [20, 30, 2],
]

Output:
7

Explanation:
[0,10)와 [9,20)는 9에서 겹침 → 동시에 선택 불가
[20,30)은 겹치지 않음
최적 선택: [9,20) + [20,30) = 5 + 2 = 7

Input: 
clusters = [
    [0, 5, 10],
    [4, 8, 9],
    [9, 12, 7],
    [6, 15, 15],
    [16, 20, 10],
]
Output:
35

Explanation:
[0,5) + [6, 15) + [16,20) 선택
총 합: 10 + 15 + 10 = 35
'''

import bisect

def max_impact_dp_binary_search(clusters):
    clusters.sort(key=lambda x: x[1])  # end 기준 정렬
    ends = [c[1] for c in clusters]    # 이진 탐색용
    n = len(clusters)
    dp = [0] * n

    for i in range(n):
        start_i, end_i, score_i = clusters[i]
        j = bisect.bisect_right(ends, start_i) - 1
        if j >= 0:
            dp[i] = max(dp[i-1], dp[j] + score_i)
        else:
            dp[i] = max(dp[i-1], score_i)
    return dp[-1]

"""
설명

end 기준 정렬 후, 각 클러스터에 대해 겹치지 않는 가장 마지막 클러스터를 이진 탐색으로 찾음

j = i번째 클러스터와 겹치지 않는 마지막 클러스터 인덱스

점화식: dp[i] = max(dp[i-1], dp[j] + score[i])

시간 복잡도: O(n * log n)

cluster 정렬 n * log n

dp 탐색 n * binary search log n

공간 복잡도: O(n)

dp, ends 크기 n
"""