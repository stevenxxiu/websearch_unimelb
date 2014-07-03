
import time
import pickle
import numpy as np
from workshops.lib.classif import get_train_test
from workshops.lib.weights import l2_norm_sparse
from workshops.lib.features import get_tf_idf
from sklearn.neighbors import KNeighborsClassifier
from proj2.lib.knn.brute import KNeighborsBrute
from proj2.lib.knn.pat import PrincipalAxisTree
from proj2.lib.knn.vpt import VPTree
from proj2.lib.knn.kdt import KDTree

class AverageLogger:
    def __init__(self):
        self.total = 0
        self.n = 0

    def update(self, value, msg=None):
        if msg:
            print(msg.format(value))
        self.total += value
        self.n += 1
        return self.total

    def average(self, msg=None):
        res = self.total/self.n
        if msg:
            print(msg.format(res))
        return res


# noinspection PyArgumentList,PyUnresolvedReferences
def main():
    with open('data/pickle/lyrl.db', 'rb') as docs_sr, open('data/pickle/lyrl_classif.db', 'rb') as classif_sr:
        docs_data = pickle.load(docs_sr)
        tf_idfs = l2_norm_sparse(get_tf_idf(docs_data.freq_matrix))
        train_indexes, test_indexes = get_train_test(len(docs_data.docs), 1000, 50)
        train_X = tf_idfs[train_indexes]
        test_X = tf_idfs[test_indexes]

        k = 1
        leaf_size = 30

        # naive, to be fair, don't assume normalized
        naive = KNeighborsBrute()
        naive.fit(train_X)
        naive_time_logger = AverageLogger()

        # kdt
        start = time.clock()
        kd_tree = KDTree()
        kd_tree.fit(train_X)
        print('KD tree construction took {} s'.format(time.clock() - start))
        kd_time_logger = AverageLogger()
        kd_node_logger = AverageLogger()

        # pat
        start = time.clock()
        pa_tree = PrincipalAxisTree(leaf_size)
        pa_tree.fit(train_X)
        print('PA tree construction took {} s'.format(time.clock() - start))
        pa_time_logger = AverageLogger()
        pa_node_logger = AverageLogger()

        # vpt
        start = time.clock()
        vp_tree = VPTree(lambda x, y: np.sqrt(np.sum(np.power((x - y).data, 2))))
        vp_tree.fit(train_X)
        print('VP tree construction took {} s'.format(time.clock() - start))
        vp_time_logger = AverageLogger()
        vp_node_logger = AverageLogger()

        # sklearn ball tree
        ball_tree = KNeighborsClassifier(k, leaf_size=leaf_size)
        ball_tree.fit(train_X, np.zeros(train_X.shape[0]))
        ball_time_logger = AverageLogger()

        for i in range(test_X.shape[0]):
            print('Searching point {}'.format(i))
            q = test_X[i]

            start = time.clock()
            naive_res = naive.kneighbors(q, k)
            naive_time_logger.update(time.clock() - start, 'Naive search took {} s')

            start = time.clock()
            kd_res = kd_tree.search(q, k)
            kd_time_logger.update(time.clock() - start, 'KD tree search took {} s')
            kd_node_logger.update(kd_tree.n_traversed, 'KD tree traversed {} nodes')

            start = time.clock()
            pa_res = pa_tree.search(q, k)
            pa_time_logger.update(time.clock() - start, 'PA tree search took {} s')
            pa_node_logger.update(pa_tree.n_traversed, 'PA tree traversed {} nodes')

            start = time.clock()
            vp_res = vp_tree.search(q, k)
            vp_time_logger.update(time.clock() - start, 'VP tree search took {} s')
            vp_node_logger.update(vp_tree.n_traversed, 'VP tree traversed {} nodes')

            start = time.clock()
            ball_res = ball_tree.kneighbors(q, k)
            ball_time_logger.update(time.clock() - start, 'Ball tree search took {} s')
            ball_res = list(zip(ball_res[0][0], ball_res[1][0]))

            # assert len(set(tuple(x[1] for x in xs) for xs in (naive_res, kd_res, pa_res, vp_res, ball_res))) == 1

        naive_time_logger.average('Naive search took an average of {} s')
        kd_time_logger.average('KD tree search took an average of {} s')
        pa_time_logger.average('PA tree search took an average of {} s')
        vp_time_logger.average('VP tree search took an average of {} s')
        ball_time_logger.average('Ball tree search took an average of {} s')

        kd_node_logger.average('KD tree traversed an average of {} nodes')
        pa_node_logger.average('PA tree traversed an average of {} nodes')
        vp_node_logger.average('VP tree traversed an average of {} nodes')


if __name__ == '__main__':
    main()
