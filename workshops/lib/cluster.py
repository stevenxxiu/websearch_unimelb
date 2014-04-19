
class DisjointSetTree:
    '''
    Represents an element in a partition.
    '''

    def __init__(self):
        self.parent = self
        self.rank = 0

    @classmethod
    def union(cls, x, y):
        x_root = x.find()
        y_root = y.find()
        if x_root == y_root:
            return x_root
        if x_root.rank < y_root.rank:
            x_root.parent = y_root
            return y_root
        elif y_root.rank > x_root.rank:
            y_root.parent = x_root
            return x_root
        else:
            y_root.parent = x_root
            x_root.rank += 1
            return x_root

    def find(self):
        '''
        Finds a representative amongst the set containing self.
        '''
        if self.parent is not self:
            self.parent = self.parent.find()
        return self.parent

    def __hash__(self):
        return super().__hash__()


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

def cluster_aggl_mst(n, mst_edges):
    '''
    converts mst_edges into a cluster, by joining the next smallest edge
    returns a tuple representation in scipy.cluster.hierarchy format
    '''
    res = []
    mst_edges.sort()
    # use an extra partition list so we can quickly find and update the current largest cluster a document belongs to
    doc_to_partition = list(DisjointSetTree() for _ in range(n))
    partition_to_cluster = dict((doc_to_partition[i], i) for i in range(n))
    for i, (weight, edge) in enumerate(mst_edges):
        u, v = edge
        part_u, part_v = doc_to_partition[u], doc_to_partition[v]
        # update clusters
        child_u, child_v = partition_to_cluster.pop(part_u.find()), partition_to_cluster.pop(part_v.find())
        num_docs_u = 1 if child_u<n else res[child_u-n][3]
        num_docs_v = 1 if child_v<n else res[child_v-n][3]
        res.append((child_u, child_v, weight, num_docs_u+num_docs_v))
        # update partitions
        part_union = DisjointSetTree.union(part_u, part_v)
        partition_to_cluster[part_union] = n + i
    return res

def cluster_aggl_mst_kruskal(n, dist_metric):
    '''
    args:
        weight_docs: a pre-fetched list for speed, assumes that this is small
    '''
    return cluster_aggl_mst(n, mst_kruskal(n, dist_metric))

def cluster_aggl_mst_prim(n, dist_metric):
    '''
    args:
        weight_docs: a pre-fetched list for speed, assumes that this is small
    '''
    return cluster_aggl_mst(n, mst_prim(n, dist_metric))
