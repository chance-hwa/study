'''
주어진 DNA 서열을 정렬하여 동일한 뉴클레오타이드가 인접하게 배치되도록 만드세요. 정렬 순서는 A → T → G → C입니다. 

내부 정렬 함수는 사용하지 않고 구현해보세요.

가능하다면, 새로운 list를 만들지 않고 구현해보세요.

입력:

sequence (리스트): 각 뉴클레오타이드를 나타내는 문자 배열.

A, T, G, C 중 하나로만 구성됩니다.

출력:

정렬된 배열: 동일한 뉴클레오타이드가 인접하게 배치되고, 순서는 A→T→G→C 를 따릅니다.
'''

def count_and_sort_sequence(sequence):
    counter = {"A": 0, "T": 0, "G": 0, "C": 0}
    
    for nucleotide in sequence:
        counter[nucleotide] += 1
    
    index = 0
    for nucleotide in "ATGC":
        while counter[nucleotide] > 0:
            sequence[index] = nucleotide
            counter[nucleotide] -= 1
            index += 1

    return sequence

def brute_force_sequence(sequence):
    order = {'A': 0, 'T': 1, 'G': 2, 'C': 3}

    n = len(sequence)
    for i in range(n):
        for j in range(i+1, n):
            if order[sequence[i]] > order[sequence[j]]:
                sequence[i], sequence[j] = sequence[j], sequence[i]

    return sequence

def two_pointer_sequence(sequence):
    low, mid, current = 0, 0, 0
    high = len(sequence) - 1

    while current <= high:
        if sequence[current] == "A":
            sequence[low], sequence[current] = sequence[current], sequence[low]
            low += 1
            mid += 1
            current += 1
        elif sequence[current] == "T":
            sequence[mid], sequence[current] = sequence[current], sequence[mid]
            mid += 1
            current += 1
        else:
            sequence[current], sequence[high] = sequence[high], sequence[current]
            high -= 1

    return sequence
