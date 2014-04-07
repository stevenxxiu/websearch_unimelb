
import time
import pymongo
from workshops.lib.weights import cosine_similarity
from workshops.lib.classif import KNN
from workshops.lib.classif_eval import ConfusionMatrix
from workshops.lib.classif_data import parse_lyrl_topics

def to_binary_classes(docs, doc_class):
    return list((doc_id, [doc_class]) if doc_class in doc_classes else (doc_id, ['not-{}'.format(doc_class)]) for doc_id, doc_classes in docs)

def classif_binary(test_docs, classifier, tfidf_db, k):
    for doc_id, doc_classes in test_docs:
        classif_class, classif_dist = classifier.classify(tfidf_db.find_one({'doc_id': doc_id})['weights'], k)[0]
        yield doc_id, classif_class

def main():
    start = time.clock()
    # get data
    client = pymongo.MongoClient()
    tfidf_db = client['websearch_workshops']['lyrl']['tfidf']
    classif_data = parse_lyrl_topics('../../../../data/lyrl30k_tpcs.txt')
    train_docs, test_docs = classif_data.get_train_test(2000, 500)
    train_docs = to_binary_classes(train_docs, 'GCAT')
    test_docs = to_binary_classes(test_docs, 'GCAT')
    test_docs_bin = ((doc_id, doc_classes[0]) for doc_id, doc_classes in test_docs)
    # classify
    classifier = KNN(lambda w1, w2: 1-cosine_similarity(w1, w2))
    classifier.train(train_docs, tfidf_db)
    classif_docs_bin = classif_binary(test_docs, classifier, tfidf_db, 11)
    # results
    cf = ConfusionMatrix.generate(list(x[1] for x in classif_docs_bin), list(x[1] for x in test_docs_bin), 'GCAT', 'not-GCAT')
    print('TP: {}, FP: {}, TN: {}, FN: {}'.format(cf.tp, cf.fp, cf.tn, cf.fn))
    print('Accuracy: {}'.format(cf.accuracy()))
    print('F1 Score: {}'.format(cf.f1()))
    print('Took {:.6f} seconds'.format(time.clock()-start))

if __name__ == '__main__':
    main()
