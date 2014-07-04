
import time
import pickle
from workshops.lib.classif import get_train_test
from workshops.lib.weights import l2_norm_sparse
from workshops.lib.features import get_tf_idf
from proj2.lib.knn.pat import PrincipalAxisTree

def main():
    start = time.clock()
    with open('data/pickle/lyrl.db', 'rb') as docs_sr, open('data/pickle/lyrl_classif.db', 'rb') as classif_sr:
        # noinspection PyArgumentList
        docs_data = pickle.load(docs_sr)
        # noinspection PyArgumentList
        tf_idfs = l2_norm_sparse(get_tf_idf(docs_data.freq_matrix))
        train_indexes, test_indexes = get_train_test(len(docs_data.docs), 2000, 500)
        train_X = tf_idfs[train_indexes]
        test_X = tf_idfs[test_indexes]
        tree = PrincipalAxisTree(6)
        tree.fit(train_X)
        tree.search(test_X[0], 40)

if __name__ == '__main__':
    main()