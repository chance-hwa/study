'''
주어진 DNA 서열에서 특정 motif가 몇 번 나타나는지 효율적으로 계산 해 보세요.

motif 는 특정 길이의 뉴클레오타이드 서열이며, 반복적으로 나타날 수 있습니다.

motif가 겹쳐서 나타날 수도 있습니다.

내장 함수를 사용하지 않고 구현 해 보세요.

입력:

sequence(str): 주어진 DNA 서열 (A, T, G, C로 이루어진 문자열)

motif (str): 찾고자하는 DNA 서열 (A, T, G, C로 이루어진 문자열)

1 <= len(motif) <= len(sequence) 로 가정

출력:

(int): 주어진 sequence에서 motif 가 나타나는 횟수
'''
'''
Input: 
sequence = "AAAAA"
motif = "AA"

Output:
4

Explanation:
sequence에서 motif "AA"는 
sequence[0:2], sequence[1:3], sequence[2:4], sequence[3:5]로 
4번 등장한다.

Input: 
sequence = "GAGAGAGATGACCTGACTGAGATGAC"
motif = "GAGAT"

Output:
2

Explanation:
sequence에서 motif "GAGAT"는
sequence[4:9], sequence[18:23]로
2번 등장한다.
'''

def find_motif_in_sequence(sequence, motif):
    count = 0
    for i in range(len(sequence) - len(motif) + 1):
        if sequence[i:i+len(motif)] == motif:
            count += 1
    
    return count

"""
brute force로 풀면 time complexity는 O(nxm). 여기서 m은 motif의 길이, n은 sequence의 길이

'이미 읽은 정보를 계속 가지고 있으면 효율적이다'
next_indices라는 빈 리스트에 motif와 일치하는 index+1을 계속 업데이트 - time complexity O(nxm).

KMP 알고리즘을 의도하고 힌트를 주심
prefix와 suffix를 보면서 lps를 motix의 길이 1부터 전체 길이까지 계산하고 O(m)
슬라이딩 하면서 찾기 O(n)
그래서 O(n+m)
결국 핵심은 "이전 비교에서 얻은 정보를 활용해" 불필요한 비교를 줄이는 것.

Boyer-Moore 알고리즘
bad character 방식. 
RABBITMOUSETIGER
TIGER 찾기
앞의 T가 아닌 R부터 비교. 일치하지 않을시 일치하는 character로 점프. 맞는게 없으면 전체 skip.
최악일 시 O(n*m), 일반적으로 O(n/m)
캐릭터가 다양하지 않을 경우 효율적이기 어려움

bad char와 good suffix 중에 점프를 많이 할 수 있는 걸 선택해서 한다.
최선의 경우 O(n/m), but sequence 서열에서는 잘 안씀.
일반적인 search 엔진에서는 많이 사용.

Rabin-Karp
문자열을 숫자로 바꾸겠다! 일반적으로 다항식으로 표현해 앞의 문자를 ASCII, 뒤의 자릿수는 2로 사용.
sliding window + two pointer를 결합하면 O(n)으로 풀림.
결국 핵심은 motif와 sequence를 "해시값"으로 만든 후 비교

BWA -> BWT + FM-index or Suffix Array
"""

# KMP algorithm
def compute_lps(motif):
    """
    LPS (Longest Prefix Suffix) 테이블을 사용해 매칭 실패시 점프
    LPS 테이블을 만들때 KMP 검색 원리를 사용하면 효율적
    - 접두사를 보는 index j와 접미사를 보는 index i를 생성
    - pattern[i] == pattern[j]인 경우 → 접미사와 접두사 모두 하나씩 늘려봄 → i와 j가 모두 하나씩 증가함
    - pattern[i] != pattern[j]인 경우 → 이전에 일치했던 접두사를 찾아 갱신함 → j를 줄여봄
        ex) pattern = ABA 에서 j = 0, i = 1 시작, 첫 string “A”는 prefix와 suffix가 없으므로 lps[0] = 0으로 초기화
            pattern[j=0] != pattern[i=1]이지만 j가 이미 0이므로 그대로 0으로 유지, lps값을 갱신하고 i만 증가 → lps[i=1] = 0, i=2
            pattern[j=0] == pattern[i=2]가 일치하므로 j가 1 증가, lps[2] = 1
    """
    m = len(motif)
    lps = [0] * m
    j = 0
    for i in range(1, m):
        while j > 0 and motif[i] != motif[j]:
            j = lps[j-1]
        if motif[i] == motif[j]:
            j += 1
            lps[i] = j
    return lps

def kmp_search(sequence, motif):
    n, m = len(sequence), len(motif)
    lps = compute_lps(motif)
    i = j = 0
    count = 0
    while i < n:
        if sequence[i] == motif[j]:
            i += 1
            j += 1
        if j == m: # motif match
            count += 1
            j = lps[j-1] # "jump"
        elif i < n and sequence[i] != motif[j]: # mismatch
            if j != 0:
                j = lps[j-1] # "jump"
            else:
                i += 1
    return count

# Boyer-Moore
"""
- 텍스트를 뒤에서부터 비교해서 빠르게 이동
- "불필요한 비교 피하고 한번에 큰 폭으로 점프"
- 평균 O(n/m)

검색의 비효율이 앞에서부터 확인할 때 온다고 가정
Bad Charater Rule / Good Suffix Rule 섞어서 사용

Bad Charater Rule
- 위에서 언급한대로 뒤에서부터 비교하다가 불일치 발생시 해당 문자가 가장 마지막으로 등장한 위치로 건너뜀
- 테이블에는 해당 character가 가장 마지막에 등장한 인덱스를 저장

Good Suffix Rule
- 뒤부터 비교, 불일치 발생시 뒤에서 이미 일치한 접미사 부분을 활용해 건너뜀
- 테이블 만들 때 두 가지 케이스 고려
    - Case 1: 패턴 안에서 동일한 접미사가 다시 등장 -> 가장 가까운 동일한 접미사 위치로 이동
    - Case 2: 동일한 접미사 없을 시 접미사 일부가 패턴의 접두사와 일치하는 경우 -> 패턴을 해당 접두사로 정렬
- Case2 만을 이용한 good suffix rule -> weak good suffix
    - 이 경우에는 접미사와 접두사가 일치하는 곳만 구하면 되어서 KMP와 비슷하게 구현해서 사용 가능
- Case1 -> strong good suffix
    - 패턴의 각 접미사에 대해 패턴 내에서 동일한 접미사가 존재하는지 확인
    - 접미사가 존재하면 해당 위치로 점프
    - 패턴 내에 동일한 접미사가 존재하지 않으면 기본적인 점프 크기 설정
"""
def preprocess_bad_character(motif):
    bad_char_table = dict()
    motif_length = len(motif)

    # motif 내 각 문자 (A,C,G,T)에 대해 마지막 등장 위치 저장
    for i in range(motif_length):
        bad_char_table[motif[i]] = i

    return bad_char_table

# Strong Good Suffix Rule
def preprocess_strong_suffix(motif, motif_length):
    good_suffix_table = [0] * (motif_length + 1) # 이동 크기 배열
    suffix_pos = [0] * (motif_length + 1) # 접미사 위치 배열

    i = motif_length # 패턴의 길이
    j = motif_length + 1 # 접미사 비교를 위한 인덱스
    suffix_pos[i] = j # 패턴 끝에 대한 접미사 위치 설정

    while i > 0:
        # motif[i-1]과 motif[j-1]이 다르면, 오른쪽에서 동일한 접미사를 찾음
        while j <= motif_length and motif[i - 1] != motif[j - 1]:
            # 접미사가 일치하지 않는 경우, good_suffix_table 배열을 업데이트하여 점프 크기를 설정
            if good_suffix_table[j] == 0:
                good_suffix_table[j] = j - i
            # 다음 접미사 위치로 이동
            j = suffix_pos[j]

        # motif[i-1]과 motif[j-1]이 같으면, 접미사가 일치함 → 저장
        i -= 1
        j -= 1
        suffix_pos[i] = j

    return good_suffix_table, suffix_pos

# 약한 접미사 규칙(Weak Good Suffix Rule) 전처리 함수
def preprocess_weak_suffix(good_suffix_table, suffix_pos, motif_length):
    """Good Suffix Table을 만들기 위한 전처리 (약한 접미사 규칙)"""
    j = suffix_pos[0]  # 첫 번째 접미사 위치 가져오기
    updated_good_suffix_table = good_suffix_table[:]  # 기존 good_suffix_table 배열 복사

    for i in range(motif_length + 1):
        # good_suffix_table 배열 중 기본값을 가진 위치를 업데이트
        if updated_good_suffix_table[i] == 0:
            updated_good_suffix_table[i] = j
        # 현재 위치가 접미사의 끝이면, 다음 넓은 접미사 위치로 변경
        if i == j:
            j = suffix_pos[j]

    return updated_good_suffix_table


# Boyer-Moore 알고리즘을 사용하여 DNA sequence에서 motif 찾기
def boyer_moore_search(sequence, motif):
    """Boyer-Moore 알고리즘을 이용한 motif 검색"""
    seq_length = len(sequence)
    motif_length = len(motif)

    # Bad Character Table 생성
    bad_char_table = preprocess_bad_character(motif)

    # Good Suffix Table 생성
    good_suffix_table, suffix_pos = preprocess_strong_suffix(motif, motif_length)
    good_suffix_table = preprocess_weak_suffix(good_suffix_table, suffix_pos, motif_length)  # Weak Suffix 적용

    i = 0  # sequence에서의 인덱스
    match_count = 0  # motif가 발견된 횟수
    match_positions = []  # motif가 발견된 인덱스 저장 리스트

    while i <= seq_length - motif_length:
        j = motif_length - 1  # motif의 마지막 문자부터 비교

        # 뒤에서부터 motif가 sequence와 일치하는지 확인
        while j >= 0 and motif[j] == sequence[i + j]:
            j -= 1

        if j < 0:  # motif가 완전히 일치하는 경우
            match_count += 1
            match_positions.append(i)
            i += good_suffix_table[0]  # Good Suffix Table을 사용하여 이동
        else:  # 불일치 발생
            bad_char_shift = j - bad_char_table.get(sequence[i + j], -1)  # Bad Character Rule
            good_suffix_shift = good_suffix_table[j + 1]  # Good Suffix Rule
            i += max(bad_char_shift, good_suffix_shift, 1)  # 더 큰 값을 선택하여 점프

    return match_count, match_positions


# Rabin - Karp
def rabin_karp_search(sequence, motif, base=2):
    """
    Rabin-Karp 알고리즘을 사용하여 sequence에서 motif 검색
    """
    seq_length = len(sequence)
    motif_length = len(motif)

    # 해시 값 초기화
    motif_hash = 0  # 패턴의 해시 값
    seq_hash = 0  # 현재 서브스트링의 해시 값
    h = base ** (motif_length - 1)  # 해시 가중치 (가장 높은 자리수 계산)

    match_count = 0  # motif 발견 개수

    # motif 및 첫 서브스트링의 해시 값 계산
    for i in range(motif_length):
        motif_hash = motif_hash * base + ord(motif[i])
        seq_hash = seq_hash * base + ord(sequence[i])

    # 슬라이딩 윈도우 방식으로 해시 비교 수행
    for i in range(seq_length - motif_length + 1):
        # 해시 값이 같으면 sequence와 motif 매치
        if motif_hash == seq_hash:
            match_count += 1

        # 다음 서브스트링의 해시 값 계산 (롤링 해시 적용)
        if i < seq_length - motif_length:
            seq_hash = (seq_hash - ord(sequence[i]) * h) * base + ord(sequence[i + motif_length])

    return match_count
