"""
문제
어떤 유전자의 변이에 의해 여러 개의 exon 중 딱 두 개의 exon만 선택되는 특이적인 splicing 변이가 발생했다고 가정합니다.

이 변이에 의해 해당 유전자가 alternative splicing이 될 때, 가장 splicing 안정성이 높은 exon의 조합으로 splicing 됩니다.

두 exon을 선택했을 때, splicing의 안정성은 다음과 같이 정의됩니다.

exon 사이의 거리 * 두 exon의 안정성 점수 중 낮은 값

각 exon의 안정성 점수가 주어질 때, splicing의 안정성이 최대가 되는 두 exon을 찾아보세요.

입력:

exon_stability(list): 각 exon 에서의 안정성 점수

2 <= len(exon_stability)

0 <= exon_stability[i]

출력:

(tuple): splicing 안정성이 가장 높은 두 exon의 index (0부터 시작)
"""

def find_most_stable_exons(exon_stability):
    stable_pair = (0, 0)
    max_stability = 0
    for i in range(len(exon_stability)-1):
        for j in range(i+1, len(exon_stability)):
            stability = min(exon_stability[i], exon_stability[j]) * (j-i)
            if stability > max_stability:
                max_stability = stability
                stable_pair = (i, j)

    return stable_pair

exon_stability = [1,8,6,2,5,4,8,3,7]
print(find_most_stable_exons(exon_stability))

exon_stability = [1, 1]
print(find_most_stable_exons(exon_stability))

"""
sorting을 하고 index 정보를 저장하면 nlogn + n으로 풀수 있음.

길이에서 얻을 수 있는 최댓값을 기반으로 길이가 긴 순서부터 최댓값을 구함.
만약 최댓값이 다음 길이의 최댓값보다 크면 중단. (heuristic algorithm)

가장 먼 두 포인트에서 포인터 설정. 포인터를 중앙으로 한 칸씩 옮기되, 최적의 선택을 하면서 옮김. n
greedy랑 two-pointer 섞어서 항상 최적의 선택만 하게 됨. 반례 없음.

l, r 포인터 설정해서 값이 작은 쪽을 옮김. 같을 경우 둘 중 하나 아무거나. 그러다가 만나면 탐색 종료 및 최댓값 반환
"""

