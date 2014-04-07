
import unittest
import pymongo
from workshops.lib.weights import cosine_similarity
from workshops.lib.cluster import cluster_aggl_mst_prim, cluster_aggl_mst_kruskal

class TestCluster(unittest.TestCase):
    def test_cluster(self):
        client = pymongo.MongoClient()
        tfidf_db = client['websearch_workshops']['lyrl']['tfidf']
        self.assertEqual(
            cluster_aggl_mst_prim(list(tfidf_db.find()[:10]), cosine_similarity),
            cluster_aggl_mst_kruskal(list(tfidf_db.find()[:10]), cosine_similarity)
        )
