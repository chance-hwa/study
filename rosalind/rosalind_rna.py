from utils import parse_args,read_fasta

def transcribe_dna_to_rna(sequence):
    rna_sequence = sequence.replace('T', 'U')

    return rna_sequence

def main():
    args = parse_args()
    sequences = read_fasta(args.input)
    sequence = sequences[0]
    rna_sequence = transcribe_dna_to_rna(sequence)
    print(rna_sequence)

if __name__ == '__main__':
    main()