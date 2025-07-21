"""
여러분은 다양한 데이터를 이진 데이터(binary data)로 저장하려고 합니다. 

나중에 각 데이터의 위치를 쉽게 찾기 위해, 하나의 block 단위로 데이터를 저장하며 block의 크기만큼 정확히 데이터를 채우고자 합니다.

각 데이터는 고정된 메모리 크기를 가지고 있습니다.

주어진 block의 크기와 각 데이터가 차지하는 메모리 크기들이 주어질 때, block을 정확히 채울 수 있는 데이터 크기 조합의 개수를 구하세요.

동일한 크기의 데이터를 여러 번 사용할 수 있습니다 (=중복 허용, 예를 들어 같은 크기의 데이터를 여러 번 넣어도 됨).

입력:

block_size(int): 한 block의 크기

data_sizes (List[int]): block에 저장 가능한 데이터들의 크기 리스트

출력:

(int): block_size에 딱 맞게 채울 수 있는 여러 data size 조합의 수

한 data는 여러 번 넣을 수 있다고 가정합니다.

같은 값의 조합이라면, 순서가 달라도 하나로 셉니다 (예: 2 + 2 + 4 = 4 + 2 + 2 는 같은 조합입니다).


예제 1:
Input: 
block_size = 5
data_sizes = [1, 2, 5]

Output:
4

Explanation:
5 = 5
5 = 2 + 2 + 1
5 = 2 + 1 + 1 + 1
5 = 1 + 1 + 1 + 1 + 1

예제 2:
Input: 
block_size = 3
data_sizes = [2]

Output:
0

Explanation:
3의 block size는 2의 data size로는 항상 꽉 채울 수 없습니다.
"""

def fill_block(block_size, data_sizes):
    dp = [0] * (block_size + 1)

    dp[0] = 1

    # data_sizes 순서대로 처리. for loop의 순서가 바뀌게 되면 중복을 고려하지 않게 됨.
    for data_size in data_sizes:
        for i in range(1, block_size + 1):
            if i >= data_size:
                dp[i] += dp[i-data_size]
                print(dp)

    return dp[block_size]

print(fill_block(5, [1, 2, 5]))
print(fill_block(3, [2]))