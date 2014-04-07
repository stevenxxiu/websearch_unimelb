
import heapq

class DisjointSetTree:
    def __init__(self):
        self.parent = self
        self.rank = 0

    @classmethod
    def union(cls, x, y):
        x_root = x.find()
        y_root = y.find()
        if x_root == y_root:
            return
        if x_root.rank < y_root.rank:
            x_root.parent = y_root
        elif y_root.rank > x_root.rank:
            y_root.parent = x_root
        else:
            y_root.parent = x_root
            x_root.rank += 1

    def find(self):
        '''
        Finds a representative amongst the set containing self.
        '''
        if self.parent != self:
            self.parent = self.parent.find()
        return self.parent


class TreeNode:
    def __init__(self, value, children=None, parent=None):
        self.value = value
        self.children = children if children is not None else []
        self.parent = parent

    def __eq__(self, other):
        if not isinstance(other, TreeNode):
            return False
        return self.value == other.value and self.children == other.children

    def descendants(self, depth=float('inf')):
        if depth<=0 or not self.children:
            yield self
        else:
            for child in self.children:
                yield from child.descendants(depth-1)

def mst_prim(n, get_weight):
    # calculate the MST using Prim's algorithm
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
        mst_edges.append((w, (min(u, v), max(u, v))))
        # new vertex added to the tree
        v = u
    return mst_edges

def mst_kruskal(n, get_weight):
    # calculate the MST using Kruskal's algorithm
    mst_edges = []
    # calculate all distances
    min_weights = []
    for i in range(n):
        for j in range(i+1, n):
            min_weights.append((get_weight(i, j), (i, j)))
    min_weights.sort()
    # calculate the mst
    partitions = list(DisjointSetTree() for _ in range(n))
    for w, (u, v) in min_weights:
        if partitions[u].find() == partitions[v].find():
            continue
        DisjointSetTree.union(partitions[u], partitions[v])
        mst_edges.append((w, (u, v)))
    return mst_edges

def cluster_aggl_mst(weight_docs, mst_edges):
    n = len(weight_docs)
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

def cluster_aggl_mst_kruskal(weight_docs, similarity_metric):
    '''
    args:
        weight_docs: a pre-fetched list for speed, assumes that this is small
    '''
    n = len(weight_docs)
    return cluster_aggl_mst(weight_docs, mst_kruskal(n, lambda i, j: similarity_metric(weight_docs[i]['weights'], weight_docs[j]['weights'])))

def cluster_aggl_mst_prim(weight_docs, similarity_metric):
    '''
    args:
        weight_docs: a pre-fetched list for speed, assumes that this is small
    '''
    n = len(weight_docs)
    return cluster_aggl_mst(weight_docs, mst_prim(n, lambda i, j: similarity_metric(weight_docs[i]['weights'], weight_docs[j]['weights'])))
