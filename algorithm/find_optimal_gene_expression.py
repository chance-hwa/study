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
    # 따라서 연속된 시간에 활성화되지 않도록 조합을 제한한다.
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

## time complexity O(2^n). 재귀함수를 사용하면 시간 조금 단축 가능.

## greedy algorithm으로도 풀 수 있음. but 가정이 몇개 필요.
### 이 단계에서 최적의 선택을 하면, 전체적으로 최적이 될 것이다.
### 특정 인덱스를 무조건 고른다는 장치를 추가하면 greedy로 풀 수 있음.
### 하지만 본 문제는 greedy를 사용하기엔 부적합함. 장치를 추가해야하기 때문에 time complexity 증가
### 특정 순간에 최적의 선택을 한다. 항상 최적의 선택이다일 시 적용할 수 있음.

## 앞을 보는 문제가 아닌 이전을 보는 문제.
## 정석적인 풀이는 O(n)으로 가능. array 하나를 만들어 dynamic programming으로 풀 수 있음.
## 쪼개서 보는것과 앞에서 쓴걸 쓸 수 있냐.

def max_expression_brute_force(expression, i = 0):
    if i >= len(expression):
        return 0

    # 현재 유전자를 선택한 경우 (i + 2로 건너뜀)
    select = expression[i] + max_expression_brute_force(expression, i + 2)
    
    # 현재 유전자를 선택하지 않은 경우 (i + 1로 이동)
    skip = max_expression_brute_force(expression, i + 1)

    return max(select, skip)

# 예제 실행
expression = [3, 2, 5, 10, 7]
print(max_expression_brute_force(expression, 0))  # Output: 15

def find_optimal_gene_expresssion_dp(expression):
    n = len(expression)
    dp = [0] * n

    dp[0] = expression[0]
    dp[1] = max(expression[0], expression[1])

    for i in range(2, n):
        dp[i] = max(dp[i-1], dp[i-2] + expression[i])
    
    return dp[-1]
