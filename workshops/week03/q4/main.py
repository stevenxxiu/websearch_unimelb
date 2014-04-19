
import pickle
import time
from workshops.lib.weights import l2_norm_sparse
from workshops.lib.features import get_tf_idf
from workshops.lib.cluster import cluster_aggl_mst_prim
from workshops.lib.sparse import RowDictMatrix

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
    with open('../../../../data/pickle/lyrl.db', 'rb') as sr:
        # noinspection PyArgumentList
        dataset = pickle.load(sr)
        tf_idfs = l2_norm_sparse(get_tf_idf(dataset.freq_matrix))
        tf_idfs_rd = RowDictMatrix.from_csr(tf_idfs)
        start = time.clock()
        cluster = cluster_aggl_mst_prim(1600, lambda i, j: RowDictMatrix.vect_dot(tf_idfs_rd[i], tf_idfs_rd[j]))
        print(tree_height(cluster) + 1)
        print('Took {:.6f} seconds'.format(time.clock()-start))

if __name__ == '__main__':
    main()
