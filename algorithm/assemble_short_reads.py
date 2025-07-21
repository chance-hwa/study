"""
주어진 short read 들을 사용하여 각 read 간 가장 overlap이 큰 read들끼리 최대한 많이 연결하여 만들 수 있는 가장 긴 consensus sequence의 길이를 구해보세요

각 read는 동일한 길이의 문자열이라고 가정

두 read의 overlap이란 한 read의 suffix와 다른 read의 prefix가 정확히 일치하는 길이

한 read가 여러개의 read와 overlap 될 경우, 최대로 overlap 된 read를 우선하여 연결한다. overlap 길이가 같은 read간에는 우선순위 없음

한 번 사용된 read는 중복 사용 불가

self-overlap(자기자신끼리)은 금지

순환 허용 X (read chain은 사이클 없이 한 방향으로만 연장)

입력:

reads (List[str]): N개의 DNA read 문자열 리스트 (각각 길이 L)

N (2 ≤ N ≤ 5,000): read 개수

read 길이 L (1 ≤ L ≤ 100)

출력:

(int): read들을 최대 overlap으로 이어붙여 만들 수 있는 최장 consensus sequence의 길이

Input: 
reads = [
  "ACGTG",
  "GTGCA",
  "GCATC"
]

Output:
9

Explanation:
최장 consensus sequence는
ACGTG
  GTGCA
    GCATC 
-> ACGTGCATC = length 9


Input: 
reads = [
  "ATGCA",
  "GCATT",
  "CATTG",
  "TTGGA",
  "GATCG",
  "GGATG",
]

Output:
12

Explanation:
최장 consensus sequence는
ATGCA
  GCATT
     TTGGA
       GGATG
-> ATGCATTGGATG = length 12
"""

def calculate_overlap(read1, read2) -> int:
    for i in range(min(len(read1), len(read2)), 0, -1):
        if read1[0:i] == read2[len(read2) - i:] or read1[len(read1) - i:] == read2[0:i]:
            return i
    return 0

def assemble_short_reads(reads: str) -> int:
    n = len(reads)
    overlap_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                overlap_matrix[i][j] = 0
                continue

            overlap_matrix[i][j] = calculate_overlap(reads[i], reads[j])

    # find the longest overlap pair
    max_overlap = 0
    max_overlap_pair = None
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if overlap_matrix[i][j] > max_overlap:
                max_overlap = overlap_matrix[i][j]
                max_overlap_pair = (i, j)

    if max_overlap > 0:
        new_reads = list()
        new_read = reads[max_overlap_pair[0]] + reads[max_overlap_pair[1]][max_overlap:]
        new_reads.append(new_read)
        for i in range(len(reads)):
            if i == max_overlap_pair[0] or i == max_overlap_pair[1]:
                continue
            new_reads.append(reads[i])
        
        return assemble_short_reads(new_reads)
    else:
        max_length = 0
        for read in reads:
            max_length = max(max_length, len(read))
        return max_length

print(assemble_short_reads(["ACGTG", "GTGCA", "GCATC"]))
print(assemble_short_reads(["ATGCA", "GCATT", "CATTG", "TTGGA", "GATCG", "GGATG"]))


"""
Prefix suffix 구할 때 rabin-karp 말고도 다른 방법이 있을까?

Trie, Suffix array등이 있다.

Trie는 branch로 뻗어나가는 형태. 

바로 붙여서는 안됨. 답이 아닐 경우도 있기 때문.
graph 탐색 방법으로 dfs.
"""