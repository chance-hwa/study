"""
용량이 각각 x 리터와 y 리터인 두 개의 물통이 있습니다.

외부에서 무한한 물 공급이 가능할 때, 아래의 세 가지 조작만으로 정확히 target 리터의 물을 만들 수 있는지 판단하세요.

하나의 물통을 가득 채운다.

하나의 물통을 완전히 비운다.

한 물통에서 다른 물통으로 물을 붓는다. 이 때 받는 물통이 가득 차거나, 붓는 물통이 비면 그 상태에서 그만 둔다.

정확히 target 리터의 물을 만들 수 있으면 True, 만들 수 없다면 False 를 반환하세요.

입력:

x(int): 첫 번째 물통의 용량

y(int): 두 번째 물통의 용량

target(int): 만들고자 하는 물의 용량

출력:

(bool): 정확히 target만큼의 물을 만들 수 있는지 여부
"""

from collections import deque

def can_measure_water(x, y, target) -> bool:

    if target > x + y:
        return False
    if target == 0:
        return True
    if x == 0 or y == 0:
        return target == x + y

    visited = set()
    queue = deque([(0, 0)])
    visited.add((0, 0))

    while queue:
        current_x, current_y = queue.popleft()
        if current_x == target or current_y == target or current_x + current_y == target:
            return True

        # Fill x
        if (x, current_y) not in visited:
            queue.append((x, current_y))
            visited.add((x, current_y))

        # Fill y
        if (current_x, y) not in visited:
            queue.append((current_x, y))
            visited.add((current_x, y))

        # Empty x
        if (0, current_y) not in visited:
            queue.append((0, current_y))
            visited.add((0, current_y))

        # Empty y
        if (current_x, 0) not in visited:
            queue.append((current_x, 0))
            visited.add((current_x, 0))

        # Pour x to y
        pour_amount = min(current_x, y - current_y)
        if (current_x - pour_amount, current_y + pour_amount) not in visited:
            queue.append((current_x - pour_amount, current_y + pour_amount))
            visited.add((current_x - pour_amount, current_y + pour_amount))

        # Pour y to x
        pour_amount = min(current_y, x - current_x)
        if (current_x + pour_amount, current_y - pour_amount) not in visited:
            queue.append((current_x + pour_amount, current_y - pour_amount))
            visited.add((current_x + pour_amount, current_y - pour_amount))

    return False


# Test
print(can_measure_water(3, 5, 4))
print(can_measure_water(2, 6, 5))
print(can_measure_water(1, 2, 3))
print(can_measure_water(8, 3, 6))


"""
수학적 방식
X, Y의 최대공약수
target%gcd(x,y) == 0
베주의 항등식으로 증명가능
최대 공약수 구하는건 log(N)
파이썬 내장함수 쓰지 않으면 정수론에 의거해서 풀어내야 함

pour = min(a, y-b)
부울수 있는 양을 이렇게 정할 수 있음.
따라서 총 여섯가지 동작이 가능함
(a,b)
(x,b) (a,y)
(0,b) (a,0)
(a-pour, b+pour) (a+pour,y-pour)

그래서 (0,0)에서 시작
if current_x == target or current_y == target or current_x + current_y == target:
    return True
BFS, DFS 둘 중 누가 유리하다고 할 순 없음 case by case
O(x*y)
가능한 상태의 수가 (x+1)*(y+1)이라서

"""

from math import gcd

def can_measure_water_math(x: int, y: int, target: int) -> bool:
    if target > x + y:
        return False
    return target % gcd(x, y) == 0

# time complexity: O(log(min(x, y)))
# space complexityL O(1)

from collections import deque

def can_measure_water_bfs(x: int, y: int, target: int) -> bool:
    if target > x + y:
        return False
    
    visited = set()
    queue = deque([(0, 0)])
    
    while queue:
        a, b = queue.popleft()

        if a == target or b == target or a + b == target:
            return True
        
        if (a, b) in visited:
            continue
        visited.add((a, b))

        # 가능한 상태 전이
        next_states = set()
        next_states.add((x, b))  # fill x
        next_states.add((a, y))  # fill y
        next_states.add((0, b))  # empty x
        next_states.add((a, 0))  # empty y

        # pour x → y
        transfer = min(a, y - b)
        next_states.add((a - transfer, b + transfer))

        # pour y → x
        transfer = min(b, x - a)
        next_states.add((a + transfer, b - transfer))

        for state in next_states:
            if state not in visited:
                queue.append(state)

    return False

# time complexity: O(x * y)
# space complexity: O(x * y)


from collections import deque

def can_measure_water_dfs(x: int, y: int, target: int) -> bool:
    if target > x + y:
        return False

    visited = set()

    def dfs(a, b):
        if (a, b) in visited:
            return False
        if a == target or b == target or a + b == target:
            return True

        visited.add((a, b))

        # 가능한 이동 상태
        return (
            dfs(x, b) or        # fill x
            dfs(a, y) or        # fill y
            dfs(0, b) or        # empty x
            dfs(a, 0) or        # empty y
            dfs(a - min(a, y - b), b + min(a, y - b)) or  # pour x → y
            dfs(a + min(b, x - a), b - min(b, x - a))     # pour y → x
        )

    return dfs(0, 0)

# time complexity: O(x * y)
# space complexity: O(x * y)