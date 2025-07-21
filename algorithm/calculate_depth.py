"""
당신은 read alignment 정보를 바탕으로 genomic position 별 depth를 계산하는 기능을 개발 중입니다.

총 길이 L인 유전체 영역이 있으며, N개의 short read의 정보가 주어집니다.

각 read의 정보는 start position과, end position을 가지고 있다고 가정합니다.

이 때 이 read는 start는 포함, end 는 포함하지 않는 [start, end) 영역에 align 됐다고 가정합니다.

start, end는 1-index로 표시합니다.

이 때 각 position에서의 read depth를 계산해보세요.

입력:

L (int): 특정 유전체 영역의 길이

1 <= L <= 1000000

reads (list[tuple]): (start, end) 튜플을 가진 read들의 리스트

start는 포함, end는 포함하지 않음 → [start, end)

start와 end 값은 1-index 로 표시

1 <= len(reads) <= 1000000

출력:

(list): 각 position에서의 read depth를 count 한 리스트

예제 1:



Input: 
L = 5
reads = [(1, 3), (2, 5)]

Output:
[1, 2, 1, 1, 0]

예제 2:
Input: 
L = 4
reads = [(1, 5), (1, 5), (1, 5)]

Output:
[3, 3, 3, 3]

예제 3:
Input:
L = 10
reads = [(1, 3), (4, 6), (7, 9), (10, 11)]

Output:
[1, 1, 0, 1, 1, 0, 1, 1, 0, 1]
"""

def calculate_depth(L: int, reads: list[tuple]) -> list:
    depth = [0] * L
    for start, end in reads:
        for i in range(start, end):
            depth[i - 1] += 1
    return depth


L = 5
reads = [(1, 3), (2, 5)]

print(calculate_depth(L, reads))

L = 4
reads = [(1, 5), (1, 5), (1, 5)]

print(calculate_depth(L, reads))

L = 10
reads = [(1, 3), (4, 6), (7, 9), (10, 11)]

print(calculate_depth(L, reads))

"""
cumulative sum을 이용하여 계산
"""

def calculate_depth(L: int, reads: list[tuple]) -> list:
    depth = [0] * L
    for start, end in reads:
        depth[start - 1] += 1
        depth[end - 1] -= 1
    
    sum = 0
    for i in range(0, L):
        sum += depth[i]
        depth[i] = sum
    return depth

L = 5
reads = [(1, 3), (2, 5)]

print(calculate_depth(L, reads))
