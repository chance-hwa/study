"""
두 개의 DNA 서열(sequence1, sequence2)이 서로 얼마나 유사한지 평가하고자 합니다.

서로 얼마나 유사한지 평가하기 위해 edit distance를 사용합니다.

edit distance는 한 서열에서 아래와 같은 연산을 사용해 같은 서열로 만드는데 얼마의 연산 횟수가 필요한지를 말합니다.

사용할 수 있는 연산은 다음과 같습니다.

한 염기를 삽입(Insert)

한 염기를 삭제(Delete)

한 염기를 치환(Replace)

위 세 가지 연산만 사용해서 sequence1을 sequence2로 변환하는 edit distance (= 최소 연산(변이) 횟수)를 구하세요.

입력:

sequence1 (str): 변환의 시작이 되는 DNA 서열 (A, C, G, T로만 구성)

sequence2 (str): 목표로 하는 DNA 서열 (A, C, G, T)

출력:

(int): sequence1을 sequence2로 변환하기 위한 최소 변이(편집) 횟수

예제 1:
Input: 
sequence1 = "AGC"
sequence2 = "ACGT"

Output:
2

Explanation:
AGC -> ACGC
ACGC -> ACGT


예제 2:
Input: 
sequence1 = "ATCGT"
sequence2 = "CTG"

Output:
3

Explanation:
ATCGT -> CTCGT
CTCGT -> CTGT
CTGT -> CTG
"""

"""
설명

sequence1과 sequence2의 비교를 한 글자씩 쪼개서 본다고 생각해봅시다.

sequence1의 부분문자 S와 sequence2의 부분문자 T 간 edit distance를 알고 있다고 가정합니다.

sequence1 = 문자열 S + ‘A', sequence2 = 문자열 T + ‘A’ 로 마지막 문자가 같으면 

문자열 S와 문자열 T 간의 edit distance로 치환할 수 있습니다 (마지막 A를 변경하지 않아도 되므로)

sequence1 = 문자열 S + ‘A', sequence2 = 문자열 T + 'G’와 같이 다르다면,

문자열 S와 문자열 T간의 edit distance + 1 (A → G 치환)

문자열 S와 문자열 T + 'G' 간의 edit distance + 1 (A 삭제)

문자열 S + 'A'와 문자열 T간의 edit distance + 1 (G 삽입)

중 최소값이 edit distance가 됩니다.

위 내용을 DP로 변경하면,

dp[i][j] = sequence1의 처음 i글자와 sequence2의 처음 j글자를 서로 일치시키기 위한 최소 연산 횟수

점화식

dp[0][j] = j (sequence1이 빈 문자열일 때, j개의 문자를 삽입)

dp[i][0] = i (sequence2가 빈 문자열일 때, i개의 문자를 삭제)

if sequence1[i] == sequence2[j]:

dp[i][j] = dp[i - 1][j - 1]

else:

dp[i][j] = 1 + min(
  dp[i-1][j],    # sequence1에서 한 글자 삭제
  dp[i][j-1],    # sequence2에 한 글자 삽입
  dp[i-1][j-1],  # 치환
)
"""


def min_edit_distance(sequence1: str, sequence2: str) -> int:
    n, m = len(sequence1), len(sequence2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if sequence1[i - 1] == sequence2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],
                    dp[i][j - 1],
                    dp[i - 1][j - 1],
                )
                
    return dp[n][m]