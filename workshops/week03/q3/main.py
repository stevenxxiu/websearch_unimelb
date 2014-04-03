
import heapq
import time
import pymongo

class TreeNode:
    def __init__(self, parent, children, value):
        self.parenet = parent
        self.children = children
        self.value = value

class Edge:
    '''
    stores a graph edge
    '''

    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2

def cosine_similarity(weight_dict_1, weight_dict_2):
    '''
    assumes that both weight_dict_1 and weight_dict_2 are normalized
    '''
    score = 0
    for term in set(weight_dict_1.keys()).intersection(weight_dict_2.keys()):
        score += weight_dict_1[term]*weight_dict_2[term]
    return score

def cluster_aggloromotive(weight_docs, similarity_metric):
    '''
    args:
        weight_docs: a pre-fetched list for speed, assumes that this is small
    '''
    # adjacency list graph, each value includes an Edge object so node merging doesn't need to care about the heap
    graph = []
    doc_ids = sorted(weight_doc['doc_id'] for weight_doc in weight_docs)
    for i, doc_id in enumerate(doc_ids):
        # make sure an edge is stored only once to better handle the undirected graph
        adjacent = []
        for j, doc_id_other in enumerate(doc_ids[i+1:]):
            adjacent.append(Edge(i, j))
        graph.append(adjacent)
    # build similarity scores
    edge_scores_heap = []
    for i, weight_doc in enumerate(weight_docs):
        for j, weight_doc_other in enumerate(weight_docs[i+1:]):
            edge_scores_heap.append((similarity_metric(weight_doc['weights'], weight_doc_other['weights']), graph[i][j]))
    heapq.heapify(edge_scores_heap)
    # the current top-most cluster a document belongs to
    doc_cluster = {}
    # build the cluster tree
    res = {}
    for i, doc_id in enumerate(doc_ids):
        res[i] = TreeNode(None, [], doc_id)
    while len(res)>1:
        heapq.heappop(edge_scores_heap)


def main():
    start=time.clock()
    client = pymongo.MongoClient()
    tfidf_db = client['websearch_workshops']['week02']['tfidf']
    cluster_aggloromotive(list(tfidf_db.find()[:100]), cosine_similarity)

    print('Took {:.6f} seconds'.format(time.clock()-start))

if __name__ == '__main__':
    main()
