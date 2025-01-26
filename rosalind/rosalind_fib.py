import sys

def fibonacci(n, k):
    a, b = 1, 1
    for i in range(2, n):
        a, b = b, a*k + b
    
    return b

def main():
    n, k = map(int, sys.argv[1:])
    print(fibonacci(n, k))

if __name__ == '__main__':
    main()

