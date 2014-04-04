
import heapq

class TreeNode:
    def __init__(self, value, children=None, parent=None):
        self.value = value
        self.children = children if children is not None else []
        self.parent = parent

    def __eq__(self, other):
        if not isinstance(other, TreeNode):
            return False
        return self.value == other.value and self.children == other.children

    def leaves(self):
        if not self.children:
            yield self
        else:
            for child in self.children:
                yield from child.leaves()

def mst_prim(n, get_weight):
    # calculate the MST using Prim's algorithm & store the edges of the MST
    mst_edges = []
    min_weights = [(None, None)]*n
    visited = [False]*n
    # arbitrary starting vertex
    v = 0
    for i in range(n-1):
        # mark as visited
        visited[v] = True
        # update the minimums for vertices adjacent to v
        for j in range(n):
            if j==v or visited[j]:
                continue
            cur_weight = get_weight(v, j)
            if min_weights[j][0] is None or cur_weight < min_weights[j][0]:
                min_weights[j] = (cur_weight, v)
        # find the minimum
        w, (u, v) = min((w, (u, v)) for u, (w, v) in enumerate(min_weights) if not visited[u] and w is not None)
        mst_edges.append((w, tuple(sorted((u, v)))))
        # new vertex added to the tree
        v = u
    return mst_edges

def cluster_aggloromotive_naive(weight_docs, similarity_metric):
    n = len(weight_docs)
    # calculate all weights
    weights = []
    for i, weight_doc_i in enumerate(weight_docs):
        for j, weight_doc_j in enumerate(weight_docs[i+1:]):
            j = i+j+1
            weights.append((similarity_metric(weight_doc_i['weights'], weight_doc_j['weights']), (i, j)))
    heapq.heapify(weights)
    clusters = list(TreeNode(i) for i in range(n))
    cluster = None
    while weights:
        weight, edge = heapq.heappop(weights)
        u, v = edge
        child_u, child_v = clusters[u], clusters[v]
        if child_u is child_v:
            continue
        cluster = TreeNode(None, [child_u, child_v])
        for leaf in cluster.leaves():
            clusters[leaf.value] = cluster
        child_u.parent = child_v.parent = cluster
    for child in cluster.leaves():
        child.value = weight_docs[child.value]['doc_id']
    return cluster

def cluster_aggloromotive_mst(weight_docs, similarity_metric):
    '''
    args:
        weight_docs: a pre-fetched list for speed, assumes that this is small
    '''
    n = len(weight_docs)
    # get the mst edges using prim's algorithm
    mst_edges = mst_prim(n, lambda i, j: similarity_metric(weight_docs[i]['weights'], weight_docs[j]['weights']))
    # convert mst_edges into a cluster
    heapq.heapify(mst_edges)
    # use an extra partition list so we can quickly find and update the current largest cluster a document belongs to
    partition_to_doc = list([i] for i in range(n))
    doc_to_partition = list(range(n))
    partition_to_cluster = list(TreeNode(weight_docs[i]['doc_id']) for i in range(n))
    cluster = None
    for i in range(n-1):
        weight, edge = heapq.heappop(mst_edges)
        u, v = edge
        # update partitions
        cur_part = n+i
        part_u, part_v = doc_to_partition[u], doc_to_partition[v]
        partition_to_doc.append(partition_to_doc[part_u] + partition_to_doc[part_v])
        partition_to_doc[part_u] = partition_to_doc[part_v] = None
        for j in partition_to_doc[cur_part]:
            doc_to_partition[j] = cur_part
        # update clusters
        child_u, child_v = partition_to_cluster[part_u], partition_to_cluster[part_v]
        cluster = TreeNode(None, [child_u, child_v])
        child_u.parent = child_v.parent = cluster
        partition_to_cluster.append(cluster)
        partition_to_cluster[part_u] = partition_to_cluster[part_v] = None
    return cluster
