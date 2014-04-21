
import pickle
import time
import numpy as np
from workshops.lib.weights import l2_norm_sparse
from workshops.lib.features import get_tf_idf
from workshops.lib.query import parse_query, get_query_vect, query_similarities

def doc_similarity(doc_id_1, doc_id_2, tf_idfs, dataset):
    return (tf_idfs[dataset.doc_indexes[doc_id_1]] * tf_idfs[dataset.doc_indexes[doc_id_2]].T).data[0]

def main():
    with open('../../../../data/pickle/lyrl.db', 'rb') as sr:
        # noinspection PyArgumentList
        dataset = pickle.load(sr)
        tf_idfs = l2_norm_sparse(get_tf_idf(dataset.freq_matrix))
        query_vect = get_query_vect(parse_query('jaguar car race'), dataset)
        start = time.clock()
        query_res = query_similarities(query_vect, None, tf_idfs, dataset)
        scores = query_res.T.toarray()[0]
        print('{:<50}{:}'.format('document id', 'score'))
        # noinspection PyTypeChecker
        for i in np.argsort(-scores):
            if scores[i] != 0:
                print('{:<50}{:}'.format(dataset.docs[i], scores[i]))
        print('Took {:.6f} seconds'.format(time.clock()-start))

if __name__ == '__main__':
    main()
