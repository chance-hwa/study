# https://velog.io/@emplam27/%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98-%EA%B7%B8%EB%A6%BC%EC%9C%BC%EB%A1%9C-%EC%95%8C%EC%95%84%EB%B3%B4%EB%8A%94-LCS-%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98-Longest-Common-Substring%EC%99%80-Longest-Common-Subsequence

from utils import parse_args, read_fasta_with_id

def longest_common_subsequence(seq1, seq2):
    seq1_length = len(seq1)
    seq2_length = len(seq2)
    lcs_matrix = [[0] * (seq2_length + 1) for _ in range(seq1_length + 1)]

    for i in range(1, seq1_length + 1):
        for j in range(1, seq2_length + 1):
            if seq1[i-1] == seq2[j-1]:
                lcs_matrix[i][j] = lcs_matrix[i-1][j-1] + 1
            else:
                lcs_matrix[i][j] = max(lcs_matrix[i-1][j], lcs_matrix[i][j-1])
                
    subsequence = ""
    idx1, idx2 = seq1_length, seq2_length
    while idx1 > 0 and idx2 > 0:
        if seq1[idx1-1] == seq2[idx2-1]:
            subsequence += seq1[idx1-1]
            idx1 -= 1
            idx2 -= 1
        elif lcs_matrix[idx1-1][idx2] > lcs_matrix[idx1][idx2-1]:
            idx1 -= 1
        else:
            idx2 -= 1

    return subsequence[::-1]

def main():
    args = parse_args()
    id2seq = read_fasta_with_id(args.input)
    seq1, seq2 = id2seq.values()

    lcs = longest_common_subsequence(seq1, seq2)
    print(lcs)

if __name__ == "__main__":
    main()