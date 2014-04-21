
import pickle
import numpy as np
from scipy.sparse import diags
from workshops.lib.query import parse_query, get_query_vect

# noinspection PyUnresolvedReferences, PyArgumentList, PyTypeChecker
def main():
    with open('../../../../data/pickle/lyrl.db', 'rb') as sr:
        dataset = pickle.load(sr)
        lambda_ = 0.4
        probs_bg = dataset.freq_matrix.sum(axis=0).A1.astype(np.float)
        probs_bg /= probs_bg.sum()
        probs_d = dataset.freq_matrix.copy()
        probs_d = diags(1/probs_d.sum(axis=1).T.A1, 0) * probs_d

        # decompose the matrix into the sum of a background row and a non-background matrix to retain sparsity
        probs_dsl = probs_d.tolil()
        for i, (row_indexes, row_probs) in enumerate(zip(probs_dsl.rows, probs_dsl.data)):
            for j, (index, prob) in enumerate(zip(row_indexes, row_probs)):
                row_probs[j] = np.log((1-lambda_)*prob + lambda_*probs_bg[index]) - np.log(lambda_*probs_bg[index])
        probs_dsl = probs_dsl.tocsr()
        probs_bgl = np.log(lambda_*probs_bg)

        # vectorize & binarize the query
        query_vect = get_query_vect(parse_query('oil price iraq tension'), dataset)
        query_vect[query_vect!=0] = 1

        # get query results
        score_bg = probs_bgl*query_vect
        query_res = probs_dsl*query_vect + probs_bgl*query_vect
        scores = query_res.A1
        print('{:<50}{:}'.format('document id', 'score'))
        for i in np.argsort(-scores):
            if scores[i] != score_bg:
                print('{:<50}{:}'.format(dataset.docs[i], scores[i]))

if __name__ == '__main__':
    main()
