
import sys
import time
import pymongo
from collections import Counter
from workshops.lib.cluster import cluster_aggl_mst_prim
from workshops.lib.weights import cosine_similarity

def cluster_average(cluster, weights_db):
    res = Counter()
    for leaf in cluster.descendants():
        res += weights_db.find_one({'doc_id': leaf.value})['weights']
    return res

def main():
    sys.setrecursionlimit(6500)
    client = pymongo.MongoClient()
    tfidf_db = client['websearch_workshops']['week02']['tfidf']
    docs = list(tfidf_db.find()[:4000])
    start = time.clock()
    cluster = cluster_aggl_mst_prim(docs, cosine_similarity)
    for depth in range(1+5):
        print('depth {}'.format(depth))
        for descendant_cluster in cluster.descendants(depth):
            print(cluster_average(descendant_cluster, tfidf_db).most_common(10))
    print('Took {:.6f} seconds'.format(time.clock()-start))

if __name__ == '__main__':
    main()
