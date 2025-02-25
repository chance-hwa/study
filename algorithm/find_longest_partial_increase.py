'''
주어진 정수 배열 nums에서 가장 긴 증가하는 (=오름차순) 부분 수열의 길이를 찾아 보세요.

부분 수열이므로 반드시 연속적일 필요는 없음.

입력:

nums(list): 양의 정수를 가지는 리스트

출력:

(int): 최장 증가 부분 수열의 길이
'''

'''
Input: 
nums = [10,9,2,5,3,7,101,18]

Output:
4

Explanation:
최장 증가 부분 수열은 [2, 3, 7, 101] 혹은 [2, 3, 7, 18]
'''

'''
Input: 
nums = [0,1,0,3,2,3]

Output:
4

Explanation:
최장 증가 부분 수열은 [0, 1, 2, 3]
'''

from itertools import combinations

def find_longest_partial_increase_brute(nums):

    n = len(nums)
    index = [i for i in range(n)]

    all_combinations = list()

    for i in range(1, n + 1):
        all_combinations.extend(list(combinations(index, i)))
    
    increasing_combinations = list()
    for combination in all_combinations:
        increasing = True
        for i in range(len(combination) - 1):
            if nums[combination[i]] >= nums[combination[i + 1]]:
                increasing = False
                break
        if increasing:
            increasing_combinations.append(combination)
    
    max_length = 0
    for combination in increasing_combinations:
        max_length = max(max_length, len(combination))
    
    return max_length

# Test code
nums = [10, 9, 2, 5, 3, 7, 101, 18]
print(find_longest_partial_increase_brute(nums))

nums = [0, 1, 0, 3, 2, 3]
print(find_longest_partial_increase_brute(nums))


def find_longest_partial_increase(nums):

    dp = [1] * len(nums)

    for i in range(1, len(nums)):
        for j in range(i):
            if nums[i] > nums[j]:
                dp[i] = max(dp[i], dp[j] + 1)
                print(dp)

    return max(dp)

# Test code
nums = [10, 9, 2, 5, 3, 7, 101, 18]
print(find_longest_partial_increase(nums))

nums = [0, 1, 0, 3, 2, 3]
print(find_longest_partial_increase(nums))

"""
dp로 풀면 O(n^2)
brute force로 풀면 O(2^n)
greedy로 풀면 O(n^2)인데, 이걸 O(nlogn)으로 줄일 수 있다.
greedy에서 필요한 생각은 최장 수열을 찾을때 값을 대체한다는 개념과 이진 탐색.
"""





