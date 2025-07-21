"""
유전체 상에 N개의 CpG 사이트가 일렬로 존재한다고 가정합니다. 각 CpG 사이트는 메틸화(1)되었거나 비메틸화(0)된 상태입니다. 
당신은 이 CpG 사이트들의 메틸화 상태를 조절하여, 특정 메틸화 패턴을 만들고자 합니다.

메틸화 조절에는 제약이 있습니다. 한 번의 조작으로 하나의 CpG 사이트를 메틸화하거나 비메틸화할 수 있지만, 
그 CpG의 양옆 사이트들도 상호작용으로 인해 함께 영향을 받습니다 (0→1, 1→0). 

예를 들어, i번 CpG에 조작을 가하면, i−1, i, i+1 번째 CpG의 상태가 모두 영향 받습니다.

단, i가 처음 index일 경우에는 i와 i+1만 반전되고, i가 마지막 인덱스일 경우에는 i−1과 i만 반전됩니다.

처음 메틸화 상태에서, 특정 메틸화 패턴을 만드는데 필요한 조작 횟수의 최소값을 구하세요.

단, 어떤 조작을 가해도 특정 메틸화 패턴을 만드는 것이 불가능하다면 -1을 반환하세요.

입력:

init_state (str): 0과 1로 이루어진 처음 메틸화 상태

target_state (str): 0과 1로 이루어진 목표 메틸화 상태

출력:

(int): init_state 에서 target_state 로 만들기 위한 최소 조작 횟수

단, 어떤 조작을 가해도 target_state 로 만드는 것이 불가능하다면 -1
"""

"""
1. 조작 on/off
2. 몇번째에 하느냐/순서 상관 X
BFS로 가능. 2^n
DP로 까다롭지만 가능. 2D array로 가능. 


왼쪽을 보면서 조작 여부를 결정. 오른쪽은 안봐도 됨. 나중에 볼거니까
첫번쨰는 조작 여부 결정할 수 없으니까 둘 다 봐야함.
끝까지 갔는데 패턴 안맞으면 -1 O(N)
최소한이 맞나? - 순서가 상관이 없어서 최소한 만족
맨 앞에 있는 것도 결정할 수 있지 않나? - 처음거는 모르니까 둘다 해보는게 맞음.
greedy
"""

def simulate(state: list, target: list, operate_first: bool) -> int:
    n = len(state)
    state = state[:]
    count = 0

    if operate_first: # 첫 번째 값 조작 여부
        state[0] = 1 - state[0]
        if n > 1:
            state[1] = 1 - state[1]
        count += 1

    for i in range(1, n):
        if state[i - 1] != target[i - 1]:
            count += 1
            for j in [i - 1, i, i + 1]:
                if 0 <= j < n:
                    state[j] = 1 - state[j]

    return count if state == target else float('inf')


def min_methylation_operations(init_state_str: str, target_state_str: str) -> int:
    init_state = [int(c) for c in init_state_str]
    target_state = [int(c) for c in target_state_str]

    # 두 가지 경우 모두 시도: 첫 번째 CpG를 조작함 / 조작 하지 않음
    result = min(simulate(init_state, target_state, True), simulate(init_state, target_state, False))
    return result if result != float('inf') else -1