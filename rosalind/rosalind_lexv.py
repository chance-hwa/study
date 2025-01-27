import sys
import itertools

def lexographic(alphabet, repeats):
    alphabet_list = list(alphabet)
    combinations_tuples = list()

    for i in range(1, repeats + 1):
        for p in itertools.product(range(len(alphabet_list)), repeat=i):
            combinations_tuples.append(p)
    
    lex = [''.join(alphabet_list[j] for j in i) for i in sorted(combinations_tuples)]

    return lex

def main():
    alphabet = sys.argv[1]
    repeats = sys.argv[2]

    lex = lexographic(alphabet, int(repeats))
    for l in lex:
        with open("lexv_output.txt", "a") as f:
            f.write(l + '\n')

if __name__ == '__main__':
    main()