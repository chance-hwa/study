from utils import parse_args,read_fasta

def count_nucleotides(sequence):
    nucleotide_counts = {'A': 0, 'C': 0, 'G': 0, 'T': 0}

    for nucleotide in sequence:
        nucleotide_counts[nucleotide] += 1

    return nucleotide_counts

def main():
    args = parse_args()
    sequences = read_fasta(args.input)
    sequence = sequences[0]
    nucleotide_counts = count_nucleotides(sequence)
    print(" ".join(str(nucleotide_counts[nucleotide]) for nucleotide in 'ACGT'))  

if __name__ == '__main__':
    main()  