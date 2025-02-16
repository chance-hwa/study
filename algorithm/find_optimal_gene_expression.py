'''
시간에 따라 발현 수준이 변동하는 유전자 A가 있습니다. 이 유전자 A를 특정 시간마다 활성화하여, 최종적으로 가장 큰 발현량을 얻고자 합니다.

하지만 어떤 시간에 한 번 활성화를 했다면, 바로 다음 시간에는 활성화 할 수 없습니다.

시간에 따른 발현량이 주어졌을 때, 유전자 발현을 최대로 활성화하는 방법을 찾아보세요.

입력:

expression(리스트): expression[i]는 i 번째 시간에서의 유전자 발현량을 나타냅니다.

expression[i] 는 항상 양수인 정수입니다.

출력:

(정수): 최대 유전자 발현량의 합
'''

from itertools import combinations

def find_optimal_gene_expression(expression):
    n = len(expression)

    # 모든 조합을 구한다.
    all_combs = []
    for i in range(1, n+1):
        all_combs += list(combinations(range(n), i))
    
    # 연속된 시간에 활성화할 수 없다.
    # 따라서, 연속된 시간에 활성화되지 않도록 조합을 제한한다.
    possible_combs = []
    for comb in all_combs:
        add = True
        for i in range(len(comb)-1):
            if comb[i] + 1 == comb[i+1]:
                add = False
        
        if add:
            possible_combs.append(comb)
        
    
    print(possible_combs)

    # 가능한 조합 중에서 최대값을 찾는다.
    max_sum = 0
    for comb in possible_combs:
        max_sum = max(max_sum, sum(expression[i] for i in comb))
    
    return max_sum


# 테스트
expression = [8,1,1,9,6]
print(find_optimal_gene_expression(expression)) 
# 17

expression = [3,2,5,10,7]
print(find_optimal_gene_expression(expression))
# 15