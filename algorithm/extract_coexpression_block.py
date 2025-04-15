"""
실험을 통해 얻은 유전자 발현량 Microarray 데이터를 가지고 있다고 가정합니다.

각 셀은 하나의 유전자 위치를 의미하며, 그 값은 해당 유전자의 정량적 발현 수준을 나타냅니다.

발현량이 특정 Threshold 이상인 유전자들만 활성화된 것으로 간주하고, 인접한 고발현 유전자들로 이루어진 가장 큰 블록의 크기를 구하고자 합니다.

인접이란 상하좌우로 연결된 경우만 포함합니다.

입력:

expression_map (List[List[float]]): Microarray로부터 얻은 발현량 데이터

expression_map[i][j] = i행 j열 cell의 유전자 발현량

threshold (float)

발현량이 이 값 이상일 경우만 발현된 유전자로 간주

출력:

(int): threshold 이상인 유전자로 이루어진 가장 큰 연결 블록의 크기

Input: 
expression_map = [
  [1.2, 2.8, 0.5],
  [0.3, 3.1, 3.2],
  [0.2, 2.9, 1.1]
]
threshold = 2.5

Output:
4

Explanation:
가장 큰 블록: [2.8, 3.1, 3.2, 2.9] -> 연결된 4개

Input: 
expression_map = [
    [3.0, 0.5, 0.5, 3.1],
    [0.4, 2.7, 0.3, 2.8],
    [3.2, 0.2, 3.3, 0.1],
    [0.1, 2.6, 0.1, 3.4]
]
threshold = 2.5

Output:
2

Explanation:
가장 큰 블록: [3.1, 2.8] -> 연결된 2개
"""

def extract_largest_coexpression_block(expression_map, threshold):
    n = len(expression_map)
    visited = [[False] * n for _ in range(n)]
    max_block_size = 0

    def dfs(i, j):
        if not (0 <= i < n and 0 <= j < n) or visited[i][j] or expression_map[i][j] < threshold:
            return 0

        visited[i][j] = True
        block_size = 1

        for add_to_i, add_to_j in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_i, new_j = i + add_to_i, j + add_to_j
            block_size += dfs(new_i, new_j)

        return block_size
    
    for i in range(n):
        for j in range(n):
            if not visited[i][j] and expression_map[i][j] >= threshold:
                block_size = dfs(i, j)  
                max_block_size = max(max_block_size, block_size)
    
    return max_block_size


# Test
expression_map = [
    [1.2, 2.8, 0.5],
    [0.3, 3.1, 3.2],
    [0.2, 2.9, 1.1]
]
threshold = 2.5

print(extract_largest_coexpression_block(expression_map, threshold))

expression_map = [
    [3.0, 0.5, 0.5, 3.1],
    [0.4, 2.7, 0.3, 2.8],
    [3.2, 0.2, 3.3, 0.1],
    [0.1, 2.6, 0.1, 3.4]
]
threshold = 2.5

print(extract_largest_coexpression_block(expression_map, threshold))

    
"""
경로 찾기 dp로 풀기 가능. 해당 블럭에 올 수 있는 경우를 다 더해주는 식으로.

UnionFind 사용 가능. 사용시 공통 root (parent) 가지는 노드의 갯수 더해서 max 값
Time complexity는 모두 O(n^2)
"""
