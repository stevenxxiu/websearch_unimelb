
import time
import pickle
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from workshops.lib.classif import get_train_test
from workshops.lib.classif_eval import ConfusionMatrix
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
        f1_scores = []
        test_size = 10000
        train_sizes = [100, 200, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
        for train_size in train_sizes:
            train_indexes, test_indexes = get_train_test(len(docs_data.docs), train_size, test_size)
            train_X, train_Y = tf_idfs[train_indexes], classif_data.labels_matrix[train_indexes]
            test_X, test_Y = tf_idfs[test_indexes], classif_data.labels_matrix[test_indexes]
            train_y = train_Y[:,classif_data.label_indexes['GCAT']].T.toarray()[0]
            test_y = test_Y[:,classif_data.label_indexes['GCAT']].T.toarray()[0]
            # classify
            classifier = SVC(kernel='linear')
            classifier.fit(train_X, train_y)
            predict_y = classifier.predict(test_X)
            # results
            cf = ConfusionMatrix.generate(predict_y, test_y)
            f1_scores.append(cf.f1())
        print('Took {:.6f} seconds'.format(time.clock()-start))
        plt.plot(train_sizes, f1_scores, marker='o', linestyle='None')
        plt.xlabel('Training size')
        plt.ylabel('F1 score')
        plt.show()

if __name__ == '__main__':
    main()
