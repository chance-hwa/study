from utils import parse_args, read_fasta

def reverse_compliment(sequence):
    compliments = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}

    reverse_compliment = ""
    for base in sequence[::-1]:
        reverse_compliment += compliments[base]
    
    return reverse_compliment

def main():
    args = parse_args()
    sequence = read_fasta(args.input)[0]
    reverse_compliment_sequence = reverse_compliment(sequence)
    print(reverse_compliment_sequence)

if __name__ == '__main__':
    main()