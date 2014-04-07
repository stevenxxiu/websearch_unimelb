
import time
import pymongo
from workshops.lib.cluster import cluster_aggloromotive_mst, cluster_aggloromotive_naive
from workshops.lib.similarity import cosine_similarity

def main():
    start=time.clock()
    client = pymongo.MongoClient()
    tfidf_db = client['websearch_workshops']['week02']['tfidf']
    cluster_aggloromotive_mst(list(tfidf_db.find()[:100]), cosine_similarity)
    print('Took {:.6f} seconds'.format(time.clock()-start))

if __name__ == '__main__':
    main()
