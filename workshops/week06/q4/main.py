
import itertools
from scipy.stats import poisson

def main():
    freq = 1020
    num_docs = 31254
    lambda_ = freq/num_docs
    for i in itertools.count(0):
        # probability of the term occuring <=i times within a document is poisson.cdf(i, lambda_)
        # get the probability of the term occuring >i times within some document in the collection
        if 1 - poisson.cdf(i, lambda_)**num_docs < 0.01:
            print(i+1)
            break

if __name__ == '__main__':
    main()
