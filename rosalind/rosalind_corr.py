from utils import parse_args, read_fasta_with_id

def reverse_compliment(sequence):
    rev = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}

    return ''.join([rev[s] for s in sequence[::-1]])

def find_loner(id2seq):
    loners = list()

    for id, sequence in id2seq.items():
        if reverse_compliment(sequence) in id2seq.values():
            continue
        if list(id2seq.values()).count(sequence) > 1:
            continue
        loners.append(id)

    return loners

def find_hamming_distance(s1, s2):
    distance = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            distance += 1        
    return distance


def find_hamming_distance_exactly_one(loners, id2seq):
    pairs = list()
    for loner in loners:
        for id, sequence in id2seq.items():
            if id in loners:
                continue
            if find_hamming_distance(sequence, id2seq[loner]) == 1:
                pairs.append(f"{id2seq[loner]}->{sequence}")
                break
            elif find_hamming_distance(reverse_compliment(sequence), id2seq[loner]) == 1:
                pairs.append(f"{id2seq[loner]}->{reverse_compliment(sequence)}")
                break
    
    return pairs

def main():
    args = parse_args()
    id2seq = read_fasta_with_id(args.input)
    
    loners = find_loner(id2seq)
    pairs = find_hamming_distance_exactly_one(loners, id2seq)

    for pair in pairs:
        print(pair)

if __name__ == "__main__":
    main()







