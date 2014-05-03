
import time
import pickle
from workshops.lib.classif import get_train_test, MultinomialNB
from workshops.lib.classif_eval import ConfusionMatrix

def main():
    start = time.clock()
    with open('../../../../data/pickle/lyrl.db', 'rb') as docs_sr, open('../../../../data/pickle/lyrl_classif.db', 'rb') as classif_sr:
        # noinspection PyArgumentList
        docs_data = pickle.load(docs_sr)
        # noinspection PyArgumentList
        classif_data = pickle.load(classif_sr)
        freq_matrix = docs_data.freq_matrix
        train_indexes, test_indexes = get_train_test(len(docs_data.docs), 1000, 1000)
        train_X, train_Y = freq_matrix[train_indexes], classif_data.labels_matrix[train_indexes]
        test_X, test_Y = freq_matrix[test_indexes], classif_data.labels_matrix[test_indexes]
        train_y = train_Y[:,classif_data.label_indexes['C15']].T.toarray()[0]
        test_y = test_Y[:,classif_data.label_indexes['C15']].T.toarray()[0]
        # classify
        classifier = MultinomialNB()
        classifier.fit(train_X, train_y)
        proba_y = classifier.predict_proba(test_X)
        # results
        for i, doc_probs in enumerate(proba_y):
            neg_prob, pos_prob = doc_probs
            print('{}: {:.5f} {}'.format(docs_data.docs[i], pos_prob, test_y[i]))

if __name__ == '__main__':
    main()
