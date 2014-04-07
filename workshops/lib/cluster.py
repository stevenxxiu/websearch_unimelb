
import heapq

class TreeNode:
    def __init__(self, value, children=None, parent=None):
        self.value = value
        self.children = children if children is not None else []
        self.parent = parent

    def __eq__(self, other):
        if not isinstance(other, TreeNode):
            return False
        return self.value == other.value and self.children == other.children and self.parent == other.parent

def cluster_aggloromotive_naive(weight_docs, similarity_metric):
    n = len(weight_docs)
    # calculate all weights
    weights = []
    for i, weight_doc_i in enumerate(weight_docs):
        for j, weight_doc_j in enumerate(weight_docs[i+1:]):
            weights.append((similarity_metric(weight_doc_i['weights'], weight_doc_j['weights']), (i, j)))
    heapq.heapify(weights)
    clusters = []
    for i in range(n):
        clusters.append(TreeNode(weight_docs[i]['doc_id']))
    cluster = None
    while weights:
        weight, edge = heapq.heappop(weights)
        u, v = edge
        if clusters[u] == clusters[v]:
            continue
        child_u, child_v = clusters[u], clusters[v]
        cluster = TreeNode(None, [child_u, child_v])
        clusters[u] = clusters[v] = cluster
        child_u.parent = child_v.parent = cluster
    return cluster

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

