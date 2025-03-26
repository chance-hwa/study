"""
문제
시간에 따라 발현 수준이 변동하는 유전자 A가 있습니다. 이 유전자 A를 특정 시간마다 활성화하여, 최종적으로 가장 큰 발현량을 얻고자 합니다.

하지만 어떤 시간에 한 번 활성화를 했다면, 바로 다음 시간에는 활성화 할 수 없습니다.

또한, 각 시간마다 유전자를 활성화하는 데 드는 비용(cost)이 있으며, 사용할 수 있는 총 자원(Budget)이 제한되어 있습니다.

시간에 따른 발현량, 활성화 비용, 총 자원이 주어졌을 때, 유전자 발현을 최대로 활성화하는 방법을 찾아보세요.

입력:

expression(리스트): expression[i]는 i 번째 시간에서의 유전자 발현량을 나타냅니다.

expression[i] 는 항상 양수인 정수입니다.

costs (리스트): costs[i]는 i 번째 시간에서의 유전자를 활성화하는데 드는 비용을 나타냅니다.

costs[i] 는 항상 양수인 정수입니다.

budget (정수): 사용할 수 있는 총 비용, budget을 초과하여 활성화 할 수 없습니다.

출력:

(정수): 최대 유전자 발현량의 합

예제 1:
Input:
expression = [8, 1, 1, 9, 6]
costs = [1, 1, 1, 1, 1]
budget = 3

Output:
17

Explanation:
expression[0] = 8 선택, cost_sum = 1
expression[3] = 9 선택, cost_sum = 2
8 + 9 = 17
cost_sum = 2 <= budget = 3


예제 2:
Input: 
expression = [3, 2, 5, 10, 7]
costs = [1, 2, 4, 4, 3]
budget = 6

Output:
13

Explanation:
expression[0] = 3 선택, cost_sum = 1
expression[3] = 10 선택, cost_sum = 5
3 + 10 = 13
cost_sum = 5 <= budget = 6
expression[0], expression[2], expression[4]를 선택할 때 최대값이 되나, 이 경우 cost가 budget을 초과하여 선택할 수 없음
"""

def find_optimal_gene_expression(expression, costs, budget):
    n = len(expression)
    

"""
dp로 풀기 어려운 이유. 연속해서 고르지 않을때가 이득인 경우가 생겨서.
따라서 2D array로 dp를 구현해야함.
dp[i][j] = i번째 expression에서 j비용 만큼 썼을 때의 최댓값
for 문을 돌때 
for j in range(budget+1):
    dp[i][j] = max(dp[i-1][j], dp[i-2][j-costs[i]] + expression[i])

내가 지금 고를 수 있는 최대치가 뭐냐. 
앞에 고를 수 있는 최대치를 정할 수 있으면 뒤에서도 똑같이 정할 수 있음
dp의 핵심은 이전 값도 최선이다. 조건이 늘어나면 차원을 늘려야 함.
"""

def max_expression_brute_force(expression, costs, budget, i = 0, current_cost = 0):
    if i >= len(expression):
        return 0

    # 현재 유전자를 선택한 경우 (i + 2로 건너뜀)
    select = 0
    if current_cost + costs[i] <= budget:
        select = expression[i] + max_expression_brute_force(expression, costs, budget, i + 2, current_cost + costs[i])
    
    # 현재 유전자를 선택하지 않은 경우 (i + 1로 이동)
    skip = max_expression_brute_force(expression, costs, budget, i + 1, current_cost)

    return max(select, skip)

"""
시간 복잡도: O(2^n)

각 index에서 2가지 선택 (고른다, 고르지 않는다.)

고를 경우 i+2를 하므로 실제로는 2^n 보다는 조금 작음

공간 복잡도: O(n)

재귀함수의 깊이 n만큼 select, skip 소모
"""



def max_gene_expression_dp(expression, costs, budget):
    n = len(expression)
    dp = [[0] * (budget + 1) for _ in range(n)]

    # 첫 번째 시간에서 활성화할 경우
    for j in range(costs[0], budget + 1):
        dp[0][j] = expression[0]

    # 두 번째 시간에서 활성화할 경우
    if n > 1:
        for j in range(costs[1], budget + 1):
            dp[1][j] = max(dp[0][j], expression[1] if j >= costs[1] else 0)

    # DP 진행 (i번째 시간에서 활성화할 경우와 하지 않을 경우 비교)
    for i in range(2, n):
        for j in range(budget + 1):
            # 현재 시간에서 활성화하지 않는 경우
            dp[i][j] = dp[i - 1][j]

            # 현재 시간에서 활성화할 경우 (바로 이전 시간은 선택 불가)
            if j >= costs[i]:
                dp[i][j] = max(dp[i][j], dp[i - 2][j - costs[i]] + expression[i])

    return max(dp[n - 1])

"""
시간 복잡도: O(n * budget)

n 길이의 expression, budget 길이만큼 각 index를 한 번 탐색

공간 복잡도: O(n * budget)

dp list 만큼 사용
"""