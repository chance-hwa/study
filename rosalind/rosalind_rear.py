#https://github.com/liuliu-umich/ROSALIND/blob/main/20230523%20REAR%20Reversal%20Distance.ipynb
from utils import parse_args

def read_permutation(file_path):
    permutations = list()
    with open(file_path) as file:
        for row in file:
            if not row.strip():
                continue
            row = list(map(int, row.strip().split()))
            permutations.append(row)

    return permutations

def find_breakpoint(current_permutation, target_permutation):
    breakpoint = list()
    for index in range(len(target_permutation) - 1):
        element = current_permutation[index]
        next_element = current_permutation[index + 1]
        if abs(target_permutation.index(element) - target_permutation.index(next_element)) != 1:
            breakpoint.append(index+1)
    
    return breakpoint

def reverse_permutation(start, end, permutation):
    prefix = permutation[:start]
    reversed_part = permutation[start:end+1][::-1]
    suffix = permutation[end:]

    return prefix + reversed_part + suffix

def 

def main():
    args = parse_args()
    permutations = read_permutation(args.input)

if __name__ == '__main__':
    main()