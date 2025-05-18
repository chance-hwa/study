'''
어떤 DNA 서열이 특정 패턴을 만족하는지 확인을 하고자 합니다.

패턴은 다음과 같은 와일드카드를 포함할 수 있습니다:

'?': 정확히 하나의 염기 (A, T, G, C)를 대체할 수 있습니다.

'*': 0개 이상의 염기를 대체할 수 있습니다 (빈 문자열 포함 가능).

DNA 서열과 패턴이 주어졌을 때, DNA 서열이 주어진 패턴과 정확히 일치하는 지 여부를 판별해보세요.

입력:

dna_seq (str):  대상 DNA 서열 (A, T, G, C 로만 구성)

pattern_seq (str): 와일드카드가 포함된 서열 패턴 (A, T, G, C, ?, * 포함)

출력:

(bool): 패턴이 DNA 서열과 완전히 일치하면 True, 아니면 False

Input: 
dna_seq = "AGCT"
pattern_seq = "A*T"

Output:
True

Explanation:
"*"는 "GC"에 대응되어 AGCT 전체를 일치시킴

Input: 
dna_seq = "GAC"
pattern_seq = "?AC"

Output:
True

Explanation:
"?"는 "G" 에 대응, 이후는 정확히 일치

Input: 
dna_seq = "TGCA"
pattern_seq = "T*G"

Output:
False

Explanation:
"*"는 아무 문자열이나 가능하지만 마지막 "G"와 "A"가 일치하지 않음
'''

def is_pattern_match(dna_seq, pattern_seq):
    dna_index = 0
    match_count = 0
    
    for pattern_index in range(len(pattern_seq)):
        if dna_index >= len(dna_seq) and match_count < len(pattern_seq):
            return False
        if pattern_seq[pattern_index] == '?':
            match_count += 1
            dna_index += 1
            continue
        elif pattern_seq[pattern_index] == '*':
            match_count += 1
            dna_index += 1
            while dna_index < len(dna_seq) and dna_seq[dna_index] != pattern_seq[pattern_index + 1]:
                dna_index += 1
        else:
            if dna_seq[dna_index] != pattern_seq[pattern_index]:
                dna_index += 1
            else:
                match_count += 1
                dna_index += 1
    
    return match_count == len(pattern_seq)

# Test
dna_seq = "AGCT"
pattern_seq = "A*T"
print(is_pattern_match(dna_seq, pattern_seq))

dna_seq = "GAC"
pattern_seq = "?AC"
print(is_pattern_match(dna_seq, pattern_seq))

dna_seq = "TGCA"
pattern_seq = "T*G"
print(is_pattern_match(dna_seq, pattern_seq))


"""
dp로 풀이 가능. 대신 dp 테이블에 공백을 고려해야함
brute에도 backtracking 개념이 들어가야함.
* 다음의 character가 일치하더라도 바로 이어지는 다음 character부터가 정답일 수 있기에.
"""

# greedy + backtracking
def is_match(dna_seq: str, pattern_seq: str) -> bool:
    dna_idx = 0           # DNA 서열에서 현재 위치
    pat_idx = 0           # 패턴 서열에서 현재 위치
    match = 0             # 마지막 '*' 이후에 시작된 DNA 서열의 위치
    star_idx = -1         # 마지막으로 등장한 '*'의 패턴 내 인덱스

    while dna_idx < len(dna_seq):
        # 경우 1: 문자가 일치하거나 '?'가 등장한 경우
        if pat_idx < len(pattern_seq) and (pattern_seq[pat_idx] == dna_seq[dna_idx] or pattern_seq[pat_idx] == '?'):
            dna_idx += 1
            pat_idx += 1
        # 경우 2: 패턴에서 '*'가 등장한 경우
        elif pat_idx < len(pattern_seq) and pattern_seq[pat_idx] == '*':
            star_idx = pat_idx          # '*'의 위치 저장
            match = dna_idx             # '*'가 대응하는 DNA 위치 저장
            pat_idx += 1                # 패턴을 다음 문자로 이동
        # 경우 3: 불일치인데 이전에 '*'가 있었던 경우 → 되돌아가서 다시 시도
        elif star_idx != -1:
            pat_idx = star_idx + 1      # '*' 다음 문자로 돌아가기
            match += 1                  # DNA 한 문자 더 먹고 다시 시도
            dna_idx = match
        # 경우 4: 불일치이고 '*'도 없었던 경우 → 매칭 실패
        else:
            return False

    # 패턴 끝에 남아있는 '*'는 모두 무시 가능
    while pat_idx < len(pattern_seq) and pattern_seq[pat_idx] == '*':
        pat_idx += 1

    # 패턴을 모두 소진했으면 매칭 성공
    return pat_idx == len(pattern_seq)

"""
Time complexity : O(n+m), worst case O(n*m)
Space complexity : O(1)
"""


def is_match(dna_seq: str, pattern_seq: str) -> bool:
    m, n = len(dna_seq), len(pattern_seq)
    
    # dp[i][j]: dna_seq[:i] vs pattern_seq[:j] match 여부
    dp = [[False] * (n + 1) for _ in range(m + 1)]

    # Initialize first character as empty string
    dp[0][0] = True
    for j in range(1, n + 1):
        if pattern_seq[j - 1] == '*':
            dp[0][j] = dp[0][j - 1]

    # dp
    for i in range(1, m + 1):      # dna_seq
        for j in range(1, n + 1):  # pattern_seq
            if pattern_seq[j - 1] == dna_seq[i - 1] or pattern_seq[j - 1] == '?':
                dp[i][j] = dp[i - 1][j - 1]
            elif pattern_seq[j - 1] == '*':
                dp[i][j] = dp[i][j - 1] or dp[i - 1][j]
    
    return dp[m][n]

"""
Time complexity : O(n*m)
Space complexity : O(n*m)
"""