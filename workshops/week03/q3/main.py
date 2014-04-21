
import pickle
import time
import matplotlib.pyplot as plt
from workshops.lib.weights import l2_norm_sparse
from workshops.lib.features import get_tf_idf
from workshops.lib.cluster import cluster_aggl_mst_prim

def dict_dot(d1, d2):
    res = 0
    for key in d1:
        if key in d2:
            res += d1[key] * d2[key]
    return res

def main():
    with open('../../../../data/pickle/lyrl.db', 'rb') as sr:
        # noinspection PyArgumentList
        dataset = pickle.load(sr)
        tf_idfs = l2_norm_sparse(get_tf_idf(dataset.freq_matrix))
        # using a list of rows stored as dicts is much faster than using indptr's
        tf_idfs_list = []
        for row in tf_idfs:
            tf_idfs_list.append(dict(zip(row.indices, row.data)))
        ns = [100, 200, 300, 400, 500, 600, 700, 800, 1600, 3200, 6400]
        deltas = []
        for n in ns:
            start = time.clock()
            cluster_aggl_mst_prim(n, lambda i, j: dict_dot(tf_idfs_list[i], tf_idfs_list[j]))
            delta = time.clock() - start
            deltas.append(delta)
            print('{} docs took {:.6f} seconds'.format(n, delta))
        plt.plot(ns, deltas, marker='o', linestyle='None')
        plt.xlabel('n')
        plt.ylabel('Time taken')
        plt.show()

if __name__ == '__main__':
    main()
