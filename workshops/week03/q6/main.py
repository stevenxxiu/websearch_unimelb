
import pickle
import time
import numpy as np
from workshops.lib.weights import l2_norm_sparse
from workshops.lib.features import get_tf_idf
from workshops.lib.cluster import cluster_aggl_mst_prim
from workshops.lib.sparse import RowDictMatrix

def get_top_clusters(n, clusters):
    '''
    get the top n clusters s.t. none of them are descendents of another
    do this by expanding the node with the next largest distance
    '''
    res = {len(clusters)*2}
    for cluster in reversed(range(len(clusters)*2+1)):
        if len(res)>=n:
            break
        # replace cluster with it's children
        res.remove(cluster)
        res.update(clusters[cluster-(len(clusters)+1)][:2])
    return sorted(res)

def cluster_dfs(node, clusters):
    n = len(clusters) + 1
    dfs_iter_stack = [iter((node,))]
    while dfs_iter_stack:
        try:
            cur_cluster = next(dfs_iter_stack[-1])
            if cur_cluster>=n:
                dfs_iter_stack.append(iter(clusters[cur_cluster-n][:2]))
            else:
                yield cur_cluster
        except StopIteration:
            dfs_iter_stack.pop()

def get_cluster_average(node, clusters, X):
    return X[list(cluster_dfs(node, clusters))].sum(axis=0)/clusters[node-(len(clusters)+1)][3]

def main():
    with open('../../../../data/pickle/lyrl.db', 'rb') as sr:
        # noinspection PyArgumentList
        dataset = pickle.load(sr)
        tf_idfs = l2_norm_sparse(get_tf_idf(dataset.freq_matrix))
        tf_idfs_rd = RowDictMatrix.from_csr(tf_idfs, float)
        start = time.clock()
        clusters = cluster_aggl_mst_prim(4000, lambda i, j: -RowDictMatrix.vect_dot(tf_idfs_rd[i], tf_idfs_rd[j]))
        for n_top in (1, 2, 4, 8, 16, 32):
            print('top {} clusters:'.format(n_top))
            for top_cluster in get_top_clusters(n_top, clusters):
                # noinspection PyUnresolvedReferences
                max_term_indexes = np.argsort(-get_cluster_average(top_cluster, clusters, tf_idfs)).A1
                num_nodes = clusters[top_cluster-(len(clusters)+1)][3] if top_cluster>=len(clusters)+1 else 1
                print('{:>5} ({:>5}): {}'.format(top_cluster, num_nodes, ' '.join(dataset.terms[i] for i in max_term_indexes[:10])))
            print()
        print('Took {:.6f} seconds'.format(time.clock()-start))

if __name__ == '__main__':
    main()
