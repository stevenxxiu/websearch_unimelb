
from scipy.stats import poisson

def main():
    freq = 1020
    num_docs = 31254
    lambda_ = freq/num_docs
    print(' '.join('{:.3f}'.format(poisson.pmf(i, lambda_)*num_docs) for i in range(0, 15+1)))

if __name__ == '__main__':
    main()
