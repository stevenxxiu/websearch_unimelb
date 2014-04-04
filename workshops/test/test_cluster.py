
import unittest
import pymongo
from workshops.lib.similarity import cosine_similarity
from workshops.lib.cluster import cluster_aggloromotive_mst, cluster_aggloromotive_naive

class TestCluster(unittest.TestCase):
    def test_cluster(self):
        client = pymongo.MongoClient()
        tfidf_db = client['websearch_workshops']['week02']['tfidf']
        self.assertEqual(
            cluster_aggloromotive_mst(list(tfidf_db.find()[:10]), cosine_similarity),
            cluster_aggloromotive_naive(list(tfidf_db.find()[:10]), cosine_similarity)
        )
