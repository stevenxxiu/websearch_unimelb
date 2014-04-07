
import time
import pymongo
import matplotlib.pyplot as plt
from workshops.lib.cluster import cluster_aggl_mst_prim
from workshops.lib.weights import cosine_similarity

def main():
    client = pymongo.MongoClient()
    tfidf_db = client['websearch_workshops']['week02']['tfidf']
    ns = [100, 200, 300, 400, 500, 600, 700, 800, 1600, 3200, 6400]
    deltas = []
    for n in ns:
        docs = list(tfidf_db.find()[:n])
        start = time.clock()
        cluster_aggl_mst_prim(docs, cosine_similarity)
        delta = time.clock()-start
        deltas.append(delta)
        print('{} docs took {:.6f} seconds'.format(n, delta))
    plt.plot(ns, deltas, marker='o', linestyle='None')
    plt.xlabel('n')
    plt.ylabel('Time taken')
    plt.show()

if __name__ == '__main__':
    main()
