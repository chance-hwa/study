"""
단백질 서열이 주어졌을 때, 특정 아미노산과의 거리 합을 계산하세요. 각 위치에서 해당 아미노산과의 거리를 기준으로 배열을 생성합니다.

입력:

protein (문자열): 단백질 서열. 

각 문자는 A, R, N, D, C, E, Q, G, H, I, L, K, M, F, P, S, T, W, Y, V 중 하나로 구성됩니다.

target (문자): 거리 기준이 되는 특정 아미노산.

출력:

(리스트): 각 위치 i에서 단백질 서열 내 모든 target 아미노산과의 거리 합.
"""

def distance_sum(protein, target):
    # find the index of the target amino acid
    target_indices = [i for i, aa in enumerate(protein) if aa == target]

    # calculate the distance sum for each position
    distance_sums = []
    for i in range(len(protein)):
        distance_sums.append(sum([abs(i - target_index) for target_index in target_indices]))
    
    return distance_sums

# sample test
print(distance_sum("RRM", "R"))
# [1, 1, 3]
print(distance_sum("ACDEACDE", "C"))
# [6, 4, 4, 4, 4, 4, 6, 8]

# Time Complexity: O(n+n*m), worst case O(n^2)
# Space Complexity: O(n+m), worst case O(n)
# Algorithm: Brute Force

def distance_sum_2(protein, target):
    total_length = len(protein)
    distance_sums = [0] * total_length
    for i, aa in enumerate(protein):
        if aa == target:
            distance = [abs(i - j) for j in range(total_length)]
            distance_sums = [sum(x) for x in zip(distance_sums, distance)]
    
    return distance_sums

# Time Complexity: O(n*m), worst case O(n^2)
# Space Complexity: O(n)
# Algorithm: Brute Force


