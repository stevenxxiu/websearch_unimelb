
import time
import pickle
import numpy as np
from workshops.lib.classif import get_train_test, Rocchio
from workshops.lib.classif_eval import ConfusionMatrix
from workshops.lib.weights import l2_norm_sparse
from workshops.lib.features import get_tf_idf

def to_binary_classes(docs, doc_class):
    return list((doc_id, [doc_class]) if doc_class in doc_classes else (doc_id, ['not-{}'.format(doc_class)]) for doc_id, doc_classes in docs)

def classif_binary(test_docs, classifier, tfidf_db):
    for doc_id, doc_classes in test_docs:
        classif_class, classif_dist = classifier.predict(tfidf_db.find_one({'doc_id': doc_id})['weights'])[0]
        yield doc_id, classif_class

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
        train_y = train_Y[:,classif_data.label_indexes['GCAT']].T.toarray()[0]
        test_y = test_Y[:,classif_data.label_indexes['GCAT']].T.toarray()[0]
        # classify
        classifier = Rocchio(lambda X, Y: 1-X*Y.T)
        classifier.fit(train_X, train_y)
        predict_y = classifier.predict(test_X)
        # results
        cf = ConfusionMatrix.generate(test_y, predict_y)
        print('TP: {}, FP: {}, TN: {}, FN: {}'.format(cf.tp, cf.fp, cf.tn, cf.fn))
        print('Accuracy: {}'.format(cf.accuracy()))
        print('F1 Score: {}'.format(cf.f1()))
        print('Took {:.6f} seconds'.format(time.clock()-start))

if __name__ == '__main__':
    main()
