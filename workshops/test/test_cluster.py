
import unittest
import pickle
from workshops.lib.weights import l2_norm_sparse
from workshops.lib.features import get_tf_idf
from workshops.lib.cluster import cluster_aggl_mst_prim, cluster_aggl_mst_kruskal

class TestCluster(unittest.TestCase):
    def test_cluster(self):
        with open('data/pickle/lyrl.db', 'rb') as sr:
            # noinspection PyArgumentList
            dataset = pickle.load(sr)
            tf_idfs = l2_norm_sparse(get_tf_idf(dataset.freq_matrix))
            self.assertEqual(
                cluster_aggl_mst_prim(10, lambda i, j: (tf_idfs[i] * tf_idfs[j].T).data[0]),
                cluster_aggl_mst_kruskal(10, lambda i, j: (tf_idfs[i] * tf_idfs[j].T).data[0])
            )
