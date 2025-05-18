'''
문제
여러 명의 환자들이 병원을 방문했고, 각 환자에겐 진료 기록에 기반한 증상이 존재합니다.

증상들은 시간 순서대로 기록된 리스트로 표현되며, 각 증상은 고유한 정수 ID로 나타납니다.

단, 하나의 환자 기록 내에서는 동일한 증상이 연속해서 두 번 이상 등장하지는 않습니다.

하지만 떨어진 위치에 다시 등장할 수는 있습니다.

모든 환자의 기록에서 공통적으로 나타나는 가장 긴 연속된 증상 서열의 길이를 구하세요.

입력:

symptom_logs (List[List[int]]): 각 환자들의 증상 발현 순서를 담고 있는 정수 리스트

symptom_logs[i]: i번째 환자의 증상 발현 순서 리스트

출력:

(int): 모든 환자에게서 공통적으로 나타나는 가장 긴 연속된 증상 흐름의 길이

예제 1:

Input: 
symptom_logs = [[0,1,2,3,4],
                [2,3,4],
                [4,0,1,2,3]]

Output:
2

Explanation:
[2, 3]이 가장 긴 연속된 공통 증상 순서

예제 2:

Input: 
symptom_logs = [[0],[1],[2]]

Output:
0

Explanation:
환자들에게서 연속되는 공통 증상 순서가 없음

예제 3:

Input: 
symptom_logs = [[0,1,2,3,4],
                [4,3,2,1,0]]

Output:
1

Explanation:
[0], [1], [2], [3], [4] 모두 길이 1의 공통 증상 순서만 가짐
'''

def get_common_symptoms(symptom_log1, symptom_log2):
    common_symptoms = list()
    i, j = 0, 0
    small_len, big_len = (len(symptom_log1), len(symptom_log2)) if len(symptom_log1) < len(symptom_log2) else (len(symptom_log2), len(symptom_log1))
    if small_len == len(symptom_log2):
        symptom_log1, symptom_log2 = symptom_log2, symptom_log1

    temp_common_symptoms = list()
    for i in range(small_len):
        for j in range(big_len):
            if symptom_log1[i] == symptom_log2[j]:
                while i < small_len and j < big_len and symptom_log1[i] == symptom_log2[j]:
                    temp_common_symptoms.append(symptom_log1[i])
                    i += 1
                    j += 1
                common_symptoms.append(list(temp_common_symptoms))
                temp_common_symptoms = list()
                break
    
    longest_common_symptom = list()
    longest_number = 0
    for k in range(len(common_symptoms)):
        if len(common_symptoms[k]) > longest_number:
            longest_number = len(common_symptoms[k])
            longest_common_symptom = common_symptoms[k]

    return longest_common_symptom

def get_longest_common_symptoms(symptom_logs):
    longest_common_symptoms = list()
    for i in range(len(symptom_logs)):
        if i == 0:
            common_symptoms = get_common_symptoms(symptom_logs[i], symptom_logs[i+1])
            longest_common_symptoms = common_symptoms
        else:
            longest_common_symptoms = get_common_symptoms(symptom_logs[i], longest_common_symptoms)
    
    return len(longest_common_symptoms)


symptom_logs = [[0,1,2,3,4],
                [4,3,2,1,0]]

symptom_logs = [[0,1,2,3,4],
                [2,3,4],
                [4,0,1,2,3]]

symptom_logs = [[0,3,2,1,4],
                [4,3,2,1,0]]

print(get_longest_common_symptoms(symptom_logs))


'''
슬라이딩 윈도우 비교방식에서 라빈카프, 롤링해쉬를 사용하면 더 효율적으로 비교 가능
하이퍼파라미터 서치시 바이너리 서치 -> 공통 리스트 갯수 찾을때 바이너리 서치 적용

이진 탐색으로 가능한 subpath 길이를 탐색

길이 k일 때, 각 path에서 길이 k의 모든 subpath를 Rabin-Karp 해시값으로 변환

모든 symptom_logs에 공통으로 포함된 해시값이 있다면 길이 k 가능 → k 보다 큰 쪽으로 이진 탐색

공통 해시값이 없다면 길이 k 불가능 → k 보다 작은 쪽으로 이진 탐색

최대 길이를 찾아감

'''

# Rabin-Karp + Binary Search
def longest_common_symptom_pattern(symptom_logs):
    BASE = 10**4 + 7  # 해시 계산 base

    def has_common_pattern_of_length(length):
        """길이 length의 공통 증상 패턴이 존재하는지 확인"""
        current_common_hashes = None
        base_power = BASE ** length

        for log in symptom_logs:
            rolling_hash = 0
            log_hashes = set()

            for i in range(len(log)):
                rolling_hash = rolling_hash * BASE + log[i]

                if i >= length:
                    rolling_hash -= log[i - length] * base_power

                if i >= length - 1:
                    log_hashes.add(rolling_hash)

            if current_common_hashes is None:
                current_common_hashes = log_hashes
            else:
                current_common_hashes &= log_hashes
                if not current_common_hashes:
                    return False

        return True

    low = 0
    high = min(len(log) for log in symptom_logs)
    answer = 0

    while low <= high:
        mid = (low + high) // 2
        if has_common_pattern_of_length(mid):
            answer = mid
            low = mid + 1
        else:
            high = mid - 1

    return answer

"""
시간 복잡도: O(O(n x L x log L))

n: 환자 수 (paths 수)

L: 가장 긴 path의 길이

m: 공통 증상 수 (증상 인덱스 수)

Binary Search:

가능한 길이는 최대 L, 탐색 횟수는 O(log L)

각 check(mid):

각 path마다 O(L)개의 부분 해시 생성

전체 path에 대해 O(n x L)

총 시간복잡도: O(n x L x log L)

공간 복잡도: O(L)

해시값 저장용 set 길이 L
"""