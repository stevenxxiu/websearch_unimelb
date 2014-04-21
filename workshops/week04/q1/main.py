
import time
import pickle
import scipy.cluster
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from workshops.lib.weights import l2_norm_sparse
from workshops.lib.features import get_tf_idf

def main():
    with open('../../../../data/pickle/lyrl.db', 'rb') as sr:
        # noinspection PyArgumentList
        dataset = pickle.load(sr)
        tf_idfs = l2_norm_sparse(get_tf_idf(dataset.freq_matrix))
        n = 100
        weights = tf_idfs[:n]
        start = time.clock()
        dist_Y = 1-(weights*weights.T).toarray()
        # noinspection PyUnresolvedReferences
        dist_Y[np.tril_indices(n)] = 0
        # flatten the upper-trianglar array
        # noinspection PyUnresolvedReferences
        dist_Y = dist_Y[np.triu_indices(n, 1)]
        cluster_Z = sp.cluster.hierarchy.single(dist_Y)
        scipy.cluster.hierarchy.dendrogram(cluster_Z)
        delta = time.clock()-start
        print('{} docs took {:.6f} seconds'.format(n, delta))
        plt.show()

if __name__ == '__main__':
    main()
