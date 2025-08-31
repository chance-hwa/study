"""
문제
N개의 단백질이 있고, 각 단백질 i는 정수 임계값 thr[i](0 ≤ thr[i] < N)를 가집니다.

단백질 복합체는 1개 이상의 단백질로 이루어질 수 있으며, K개의 단백질로 구성된 최종 복합체의 크기를 K(1 ≤ K ≤ N) 라 합니다.

단백질 복합체는 모든 단백질 i가 다음 조건 중 하나를 만족하면 안정 상태 입니다.

단백질 i가 복합체에 포함되고, K > thr[i]

단백질 i가 복합체에서 제외되고, K < thr[i]

단백질 복합체가 안정 상태에 있을 수 있도록 복합체에 포함시킬 단백질 집합을 고르는 경우의 수를 구해보세요.

입력:

thr(List[int]): 각 단백질의 임계값 리스트

1 ≤ N = len(thr) ≤ 100,000

0 ≤ thr[i] < N

출력:

(int): 단백질 복합체를 안정 상태를 만족하도록 복합체를 구성하는 방법의 수

Input: 
thr = [1, 1]

Output:
1

Explanation:
안정된 복합체는 두 단백질을 모두 포함한 복합체 (K=2)만 가능

Input: 
thr = [6, 0, 3, 3, 6, 7, 2, 7]

Output:
3

Explanation:
임계값이 0인 단백질 하나로 구성 -> K=1
임계값이 0, 3, 3, 2인 단백질 4개로 구성 -> K=4
모든 단백질을 포함하는 구성 -> K=8
"""

def find_number_of_stable_protein_brute(thr: list) -> int:
    n = len(thr)
    unique_thr = set(thr)

    included_protein_counts = set()
    for k in range(1, n + 1):
        if k in unique_thr:
            continue
        included_protein_count = 0
        for i in range(n):
            if k > thr[i]:
                included_protein_count += 1
        if included_protein_count != 0:
            included_protein_counts.add(included_protein_count)
            print(k, included_protein_count)

    return len(included_protein_counts)
    

thr = [6, 0, 3, 3, 6, 7, 2, 7]
print(find_number_of_stable_protein_brute(thr))

thr = [1, 1]
print(find_number_of_stable_protein_brute(thr))

"""
Sorting and Greedy

최종 복합체 크기를 K라고 하면,

포함되는 단백질은 반드시 thr[i] < K 여야 함.

제외되는 단백질은 반드시 thr[i] > K 여야 함.

thr[i] == K인 단백질이 있으면 불가능.

thr 배열을 정렬한다. → a[0] ≤ a[1] ≤ ... ≤ a[n-1]

K = n: 항상 유효 (모두 포함).

1 ≤ K ≤ n-1: a[K-1] < K < a[K]일 때만 유효.
(왼쪽까지 K개 포함, 오른쪽은 전부 제외, 중간 값은 없어야 함)

조건을 만족하는 K 개수를 센다.

시간 복잡도: O(N * log N)

정렬: O(N * log N)

스캔: O(N)

공간 복잡도: O(1)

추가적인 메모리를 소요하지 않음
"""

def count_complex_ways_sort(thr: list) -> int:
    n = len(thr)
    thr = sorted(thr)
    res = 0

    # K = n (전부 포함): thr[i] < n 이므로 항상 가능
    res += 1

    for K in range(1, n):
        if (thr[K-1] < K) and (K < thr[K]):
            res += 1

    return res


"""
Prefix Sum

1번에서 설명한 정렬 대신 히스토그램 + 누적합으로 같은 걸 체크할 수 있다.

cnt[x]: 임계값이 정확히 x인 단백질의 개수.

psum[K] = cnt[0] + ... + cnt[K-1] = #{thr < K}

시간 복잡도: O(N)

카운팅: O(N)

스캔: O(N)

공간 복잡도: O(N)

cnt list
"""

def count_complex_ways_prefix(thr: list) -> int:
    n = len(thr)
    cnt = [0] * n
    for t in thr:
        cnt[t] += 1

    res = 0
    # K = n (전부 포함): 항상 가능
    res += 1

    psum = 0
    for K in range(1, n):
        psum += cnt[K - 1]
        if psum == K and cnt[K] == 0:
            res += 1

    return res