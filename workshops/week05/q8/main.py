
import numpy as np
import scipy as sp
import scipy.sparse
import pymongo
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from workshops.lib.classif_eval import ConfusionMatrix
from workshops.lib.classif_data import parse_lyrl_topics

def labelled_docs_to_bin_label_vect(docs, doc_class):
    return np.array(list(1 if doc_class in doc_classes else 0 for doc_id, doc_classes in docs))

def get_all_terms(docs_db):
    all_terms = set()
    for doc in docs_db.find():
        all_terms.update(doc['weights'].keys())
    # sort to be more deterministic
    return sorted(all_terms)

def docs_to_matrix(docs, all_terms, docs_db):
    # convert to sklearn format
    all_terms_dict = dict((term, i) for i, term in enumerate(all_terms))
    x_rows = []
    for doc in docs:
        col = []
        data = []
        for term, weight in docs_db.find_one({'doc_id': doc})['weights'].items():
            col.append(all_terms_dict[term])
            data.append(weight)
        row = np.zeros(len(col))
        x_row = sp.sparse.coo_matrix((data, (row, col)), shape=(1, len(all_terms)))
        x_rows.append(x_row)
    x = sp.sparse.vstack(x_rows)
    return x

def main():
    # get data
    client = pymongo.MongoClient()
    tfidf_db = client['websearch_workshops']['lyrl']['tfidf']
    classif_data = parse_lyrl_topics('../../../../data/lyrl30k_tpcs.txt')
    all_terms = get_all_terms(tfidf_db)
    f1_scores = []
    test_size = 10000
    train_sizes = [100, 200, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
    for train_size in train_sizes:
        train_docs, test_docs = classif_data.get_train_test(train_size, test_size)
        # train matrix
        train_X = docs_to_matrix(list(doc_id for doc_id, doc_class in train_docs), all_terms, tfidf_db)
        train_y = labelled_docs_to_bin_label_vect(train_docs, 'GCAT')
        # test matrix
        test_X = docs_to_matrix(list(doc_id for doc_id, doc_class in test_docs), all_terms, tfidf_db)
        test_y = labelled_docs_to_bin_label_vect(test_docs, 'GCAT')
        # classify
        classifier = SVC(kernel='linear')
        classifier.fit(train_X, train_y)
        classified_y = classifier.predict(test_X)
        # results
        cf = ConfusionMatrix.generate(classified_y, test_y, 1, 0)
        f1_scores.append(cf.f1())
    plt.plot(train_sizes, f1_scores, marker='o', linestyle='None')
    plt.xlabel('Training size')
    plt.ylabel('F1 score')
    plt.show()

if __name__ == '__main__':
    main()
