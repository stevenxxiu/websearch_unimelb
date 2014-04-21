
import pickle
import argparse
from collections import Counter

def main():
    arg_parser=argparse.ArgumentParser()
    arg_parser.add_argument('min_ct', type=int)
    arg_parser.add_argument('max_ct', type=int)
    arg_parser.add_argument('max_fdt', type=int)
    args=arg_parser.parse_args()
    with open('../../../../data/pickle/lyrl.db', 'rb') as docs_sr:
        # noinspection PyArgumentList
        docs_data = pickle.load(docs_sr)
        coll_freqs = docs_data.freq_matrix.sum(axis=0).A1
        for i, coll_freq in enumerate(coll_freqs):
            if args.min_ct<=coll_freq<=args.max_ct:
                term_freqs = Counter(docs_data.freq_matrix[:,i].todense().A1)
                print('{:<10}{:<10}{}'.format(docs_data.terms[i], coll_freq, list(term_freqs[term_freq] for term_freq in range(0, args.max_fdt+1))))

if __name__ == '__main__':
    main()
