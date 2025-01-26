import sys

def dominant_probability(k, m, n):
    total = k + m + n
    total_pairs = total * (total - 1) / 2

    # Calculate the probability of each genotype
    # k = homozygous dominant
    # m = heterozygous
    # n = homozygous recessive
    # k + k = 1
    # k + m = 1
    # k + n = 1
    # m + m = 0.75
    # m + n = 0.5
    # n + n = 0

    p_kk = k * (k - 1) / 2 / total_pairs
    p_km = k * m / total_pairs
    p_kn = k * n / total_pairs
    p_mm = m * (m - 1) / 2 / total_pairs * 0.75
    p_mn = m * n / total_pairs * 0.5
    p_nn = n * (n - 1) / 2 / total_pairs * 0

    return p_kk + p_km + p_kn + p_mm + p_mn + p_nn

def main():
    k, m, n = map(int, sys.argv[1:])
    print(dominant_probability(k, m, n))

if __name__ == '__main__':
    main()