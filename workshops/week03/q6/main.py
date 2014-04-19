
import sys
import pickle
import time
import numpy as np
from workshops.lib.weights import l2_norm_sparse
from workshops.lib.features import get_tf_idf
from workshops.lib.cluster import cluster_aggl_mst_prim
from workshops.lib.sparse import RowDictMatrix

def get_cluster_average(cluster, X):
    leaf_values = list(leaf.value for leaf in cluster.descendants())
    return X[leaf_values].sum(axis=0)

def main():
    sys.setrecursionlimit(6500)
    with open('../../../../data/pickle/lyrl.db', 'rb') as sr:
        # noinspection PyArgumentList
        dataset = pickle.load(sr)
        tf_idfs = l2_norm_sparse(get_tf_idf(dataset.freq_matrix))
        tf_idfs_rd = RowDictMatrix.from_csr(tf_idfs)
        start = time.clock()
        cluster = cluster_aggl_mst_prim(4000, lambda i, j: RowDictMatrix.vect_dot(tf_idfs_rd[i], tf_idfs_rd[j]))
        for depth in range(1+5):
            print('depth {}'.format(depth))
            for descendant_cluster in cluster.descendants(depth):
                # noinspection PyUnresolvedReferences
                max_term_indexes = np.argsort(-get_cluster_average(descendant_cluster, tf_idfs)).A1
                print(list(dataset.terms[i] for i in max_term_indexes[:10]))
        print('Took {:.6f} seconds'.format(time.clock()-start))

if __name__ == '__main__':
    main()
