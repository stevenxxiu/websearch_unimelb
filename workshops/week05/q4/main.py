
import time
import pymongo
from workshops.lib.weights import cosine_similarity
from workshops.lib.classif import Rocchio
from workshops.lib.classif_data import parse_lyrl_topics

def to_binary_classes(docs, doc_class):
    return list((doc_id, [doc_class]) if doc_class in doc_classes else (doc_id, ['not-{}'.format(doc_class)]) for doc_id, doc_classes in docs)

def main():
    start = time.clock()
    client = pymongo.MongoClient()
    tfidf_db = client['websearch_workshops']['lyrl']['tfidf']
    classif_data = parse_lyrl_topics('../../../../data/lyrl30k_tpcs.txt')
    train_docs, test_docs = classif_data.get_train_test(15000, 15000)
    train_docs = to_binary_classes(train_docs, 'GCAT')
    test_docs = to_binary_classes(test_docs, 'GCAT')
    classifier = Rocchio(lambda w1, w2: 1-cosine_similarity(w1, w2))
    classifier.train(train_docs, tfidf_db)
    tp = fp = tn = fn = 0
    for doc_id, doc_classes in test_docs:
        doc_class = doc_classes[0]
        classif_class, classif_dist = classifier.classify(tfidf_db.find_one({'doc_id': doc_id})['weights'])[0]
        if classif_class == 'GCAT' and doc_class == 'GCAT':
            tp += 1
        elif classif_class == 'GCAT' and doc_class != 'GCAT':
            fp += 1
        elif classif_class != 'GCAT' and doc_class == 'GCAT':
            fn += 1
        elif classif_class != 'GCAT' and doc_class != 'GCAT':
            tn += 1
    print('TP: {}, FP: {}, TN: {}, FN: {}'.format(tp, fp, tn, fn))
    print('Accuracy: {}'.format((tp+tn)/(tp+fp+tn+fn)))
    print('F1 Score: {}'.format(2*tp/(2*tp+fp+fn)))
    print('Took {:.6f} seconds'.format(time.clock()-start))

if __name__ == '__main__':
    main()
