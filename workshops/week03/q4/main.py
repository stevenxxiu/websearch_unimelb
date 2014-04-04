
import time
import pymongo
from workshops.lib.cluster import cluster_aggloromotive_mst
from workshops.lib.weights import cosine_similarity

def tree_height(cluster):
    height = 0
    dfs_iter_stack = [iter((cluster,))]
    while dfs_iter_stack:
        try:
            cur_cluster = next(dfs_iter_stack[-1])
            dfs_iter_stack.append(iter(cur_cluster.children))
            height = max(height, len(dfs_iter_stack)-2)
        except StopIteration:
            dfs_iter_stack.pop()
    return height

def main():
    client = pymongo.MongoClient()
    tfidf_db = client['websearch_workshops']['week02']['tfidf']
    docs = list(tfidf_db.find()[:6400])
    start = time.clock()
    cluster = cluster_aggloromotive_mst(docs, cosine_similarity)
    print(tree_height(cluster))
    print('Took {:.6f} seconds'.format(time.clock()-start))

if __name__ == '__main__':
    main()
