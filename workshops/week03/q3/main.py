
import pickle
import time
import matplotlib.pyplot as plt
from workshops.lib.weights import l2_norm_sparse
from workshops.lib.features import get_tf_idf
from workshops.lib.cluster import cluster_aggl_mst_prim
from workshops.lib.sparse import RowDictMatrix

def main():
    with open('../../../../data/pickle/lyrl.db', 'rb') as sr:
        # noinspection PyArgumentList
        dataset = pickle.load(sr)
        tf_idfs = l2_norm_sparse(get_tf_idf(dataset.freq_matrix))
        tf_idfs_rd = RowDictMatrix.from_csr(tf_idfs)
        ns = [100, 200, 300, 400, 500, 600, 700, 800, 1600, 3200, 6400]
        deltas = []
        for n in ns:
            start = time.clock()
            cluster_aggl_mst_prim(n, lambda i, j: RowDictMatrix.vect_dot(tf_idfs_rd[i], tf_idfs_rd[j]))
            delta = time.clock() - start
            deltas.append(delta)
            print('{} docs took {:.6f} seconds'.format(n, delta))
        plt.plot(ns, deltas, marker='o', linestyle='None')
        plt.xlabel('n')
        plt.ylabel('Time taken')
        plt.show()

if __name__ == '__main__':
    main()
