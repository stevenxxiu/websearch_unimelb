
import pickle
from collections import Counter
from scipy.stats import poisson

def main():
    with open('../../../../data/pickle/lyrl.db', 'rb') as docs_sr:
        # noinspection PyArgumentList
        docs_data = pickle.load(docs_sr)
        freq_matrix = docs_data.freq_matrix.tocsc()
        coll_freqs = freq_matrix.sum(axis=0).A1
        for i, coll_freq in enumerate(coll_freqs):
            term_freqs = Counter(freq_matrix[:,i].todense().A1)
            lambda_ = coll_freq/len(docs_data.docs)
            # isf(p) gives the smallest x s.t. 1 - cdf(x) < p
            # we find the smallest x s.t. cdf(x)**num_docs < p,
            # i.e. the frequency where we have less than 0.99 probability of having all frequencies <=x
            max_poisson_term_freq = poisson.isf(1-(1-0.01)**(1/len(docs_data.docs)), lambda_)
            if max(term_freqs.keys())<max_poisson_term_freq:
                print(docs_data.terms[i])

if __name__ == '__main__':
    main()
