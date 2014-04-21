
import time
import pickle
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
        train_indexes, test_indexes = get_train_test(len(docs_data.docs), 2000, 500)
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
        print('TP: {}, FP: {}, TN: {}, FN: {}'.format(cf.tp, cf.fp, cf.tn, cf.fn))
        print('Accuracy: {}'.format(cf.accuracy()))
        print('F1 Score: {}'.format(cf.f1()))
        print('Took {:.6f} seconds'.format(time.clock()-start))

if __name__ == '__main__':
    main()
