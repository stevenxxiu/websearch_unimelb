
import heapq
import time
import pymongo

class TreeNode:
    def __init__(self, value, children=None, parent=None):
        self.parenet = parent
        self.children = children if children is not None else []
        self.value = value

def cosine_similarity(weight_dict_1, weight_dict_2):
    '''
    assumes that both weight_dict_1 and weight_dict_2 are normalized
    '''
    score = 0
    for term in set(weight_dict_1.keys()).intersection(weight_dict_2.keys()):
        score += weight_dict_1[term]*weight_dict_2[term]
    return score

def cluster_aggloromotive_mst(weight_docs, similarity_metric):
    '''
    args:
        weight_docs: a pre-fetched list for speed, assumes that this is small
    '''
    n = len(weight_docs)
    # calculate the MST using Prim's algorithm & store the edges of the MST
    mst_edges = []
    # start at vertex 0
    cur_vertex = 0
    visited = [False]*n
    for i in range(n-1):
        visited[cur_vertex] = True
        cur_weight_doc = weight_docs[cur_vertex]
        min_weight = None
        min_edge = None
        adj_vertex = None
        for adj_vertex, weight_doc in enumerate(weight_docs):
            if visited[adj_vertex]:
                continue
            cur_weight = similarity_metric(cur_weight_doc['weights'], weight_doc['weights'])
            if min_weight is None or cur_weight < min_weight:
                min_weight = cur_weight
                min_edge = (cur_vertex, adj_vertex)
        mst_edges.append((min_weight, min_edge))
        cur_vertex = adj_vertex
    # convert mst_edges into a cluster
    heapq.heapify(mst_edges)
    # the current cluster a vertex belongs to
    clusters = []
    for i in range(n):
        clusters.append(TreeNode(weight_docs[i]['doc_id']))
    cluster = None
    for i in range(n-1):
        min_weight, min_edge = heapq.heappop(mst_edges)
        u, v = min_edge
        child_u, child_v = clusters[u], clusters[v]
        cluster = TreeNode(None, [child_u, child_v])
        clusters[u] = clusters[v] = cluster
        child_u.parent = child_v.parent = cluster
    return cluster


def main():
    start=time.clock()
    client = pymongo.MongoClient()
    tfidf_db = client['websearch_workshops']['week02']['tfidf']
    cluster_aggloromotive_mst(list(tfidf_db.find()[:100]), cosine_similarity)

    print('Took {:.6f} seconds'.format(time.clock()-start))

if __name__ == '__main__':
    main()
