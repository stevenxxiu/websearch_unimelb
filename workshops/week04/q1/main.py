
import time
import pymongo
import scipy.cluster
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from workshops.lib.weights import cosine_similarity

def get_distance_matrix(docs, distance_func):
    dist_Y = np.zeros(shape=(len(docs), len(docs)))
    for i in range(len(docs)):
        for j in range(i+1, len(docs)):
            dist_Y[i][j] = distance_func(docs[i]['weights'], docs[j]['weights'])
    return dist_Y

def main():
    client = pymongo.MongoClient()
    tfidf_db = client['websearch_workshops']['lyrl']['tfidf']
    n = 100
    docs = list(tfidf_db.find().sort('doc_id', 1)[:n])
    start = time.clock()
    dist_Y = get_distance_matrix(docs, lambda x, y: 1 - cosine_similarity(x, y))
    cluster_Z = sp.cluster.hierarchy.single(dist_Y)
    scipy.cluster.hierarchy.dendrogram(cluster_Z)
    delta = time.clock()-start
    print('{} docs took {:.6f} seconds'.format(n, delta))
    plt.show()

if __name__ == '__main__':
    main()
