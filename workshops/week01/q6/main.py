
import pickle
import numpy as np
from workshops.lib.weights import l2_norm_sparse
from workshops.lib.features import get_tf_idf

def doc_similarities(doc_id, tf_idfs, dataset):
    return tf_idfs * tf_idfs[dataset.doc_indexes[doc_id]].T

def main():
    doc_id = '26413'
    with open('../../../../data/pickle/lyrl.db', 'rb') as sr:
        dataset = pickle.load(sr)
        tf_idfs = l2_norm_sparse(get_tf_idf(dataset.freq_matrix))
        scores = doc_similarities(doc_id, tf_idfs, dataset).T.toarray()[0]
        print('{:<50}{:}'.format('document id', 'score'))
        for i in np.argsort(-scores):
            if dataset.docs[i] != doc_id and scores[i] != 0:
                print('{:<50}{:}'.format(dataset.docs[i], scores[i]))

if __name__ == '__main__':
    main()
