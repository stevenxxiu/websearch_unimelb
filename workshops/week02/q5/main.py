
import pickle
import time
import numpy as np
from workshops.lib.weights import l2_norm_sparse
from workshops.lib.features import get_tf_idf

def term_similarities(term, X, dataset):
    term_vect = X[:,dataset.term_indexes[term]]
    # find the rows we include in the matrix
    # we do not care filter terms, as this is hard to do if a matrix wasn't used
    inc_doc_indexes = list(dataset.doc_indexes[doc] for doc in dataset.inverted_index[term])
    # use the inverted index for faster multiplication
    Y = X[inc_doc_indexes,]
    r = Y.T * term_vect[inc_doc_indexes,]
    return r

def main():
    with open('../../../../data/pickle/lyrl.db', 'rb') as sr:
        # noinspection PyArgumentList
        dataset = pickle.load(sr)
        tf_idfs = l2_norm_sparse(get_tf_idf(dataset.freq_matrix))
        for term in ['socc', 'jaguar', 'najibullah']:
            start = time.clock()
            term_res = term_similarities(term, tf_idfs, dataset)
            # term_res = tf_idfs.T * term_vect
            scores = term_res.T.toarray()[0]
            print('similar terms to {}'.format(term))
            print()
            print('{:<50}{:}'.format('term', 'score'))
            # noinspection PyTypeChecker
            for i in np.argsort(-scores):
                if dataset.terms[i] != term and scores[i] != 0:
                    print('{:<50}{:}'.format(dataset.terms[i], scores[i]))
            print('Took {:.6f} seconds'.format(time.clock()-start))
            print()

if __name__ == '__main__':
    main()
