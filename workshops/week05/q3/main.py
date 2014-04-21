
import time
import pickle
import numpy as np
from scipy.sparse import vstack
from workshops.lib.classif import get_train_test, Rocchio
from workshops.lib.weights import l2_norm_sparse
from workshops.lib.features import get_tf_idf

def main():
    start = time.clock()
    with open('../../../../data/pickle/lyrl.db', 'rb') as docs_sr, open('../../../../data/pickle/lyrl_classif.db', 'rb') as classif_sr:
        # noinspection PyArgumentList
        docs_data = pickle.load(docs_sr)
        # noinspection PyArgumentList
        classif_data = pickle.load(classif_sr)
        tf_idfs = l2_norm_sparse(get_tf_idf(docs_data.freq_matrix))
        train_indexes, test_indexes = get_train_test(len(docs_data.docs), 15000, 15000)
        train_X, train_Y = tf_idfs[train_indexes], classif_data.labels_matrix[train_indexes]
        test_X, test_Y = tf_idfs[test_indexes], classif_data.labels_matrix[test_indexes]
        # flatten train_Y by counting the same documents multiple times
        train_doc_rows = []
        train_label_rows = []
        for train_doc_row, train_label_row in zip(train_X, train_Y):
            for label in train_label_row.nonzero()[1]:
                train_doc_rows.append(train_doc_row)
                train_label_rows.append(label)
        train_X = vstack(train_doc_rows, format='csr')
        train_y = np.array(train_label_rows)
        # classify
        classifier = Rocchio(lambda X, Y: 1-X*Y.T)
        classifier.fit(train_X, train_y)
        predict_y = classifier.predict(test_X)
        # get accuracy
        num_incorrect = 0
        for test_label_row, predict_label in zip(test_Y, predict_y):
            if not test_label_row[:,predict_label].data:
                num_incorrect += 1
        print('Classified incorrectly {:.2f}% labels'.format(num_incorrect/test_X.shape[0]*100))
        print('Took {:.6f} seconds'.format(time.clock()-start))

if __name__ == '__main__':
    main()
