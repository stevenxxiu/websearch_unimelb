
import time
import pymongo
from workshops.lib.weights import cosine_similarity
from workshops.lib.classif import Rocchio
from workshops.lib.classif_data import parse_lyrl_topics

def main():
    start = time.clock()
    client = pymongo.MongoClient()
    tfidf_db = client['websearch_workshops']['lyrl']['tfidf']
    classif_data = parse_lyrl_topics('../../../../data/lyrl30k_tpcs.txt')
    train_docs, test_docs = classif_data.get_train_test(15000, 15000)
    classifier = Rocchio(lambda w1, w2: 1-cosine_similarity(w1, w2))
    classifier.train(train_docs, tfidf_db)
    num_incorrect = 0
    for doc_id, doc_classes in test_docs:
        classif_class, classif_dist = classifier.classify(tfidf_db.find_one({'doc_id': doc_id})['weights'])[0]
        if classif_class not in doc_classes:
            num_incorrect += 1
    print('Classified incorrectly {:.2f}% labels'.format(num_incorrect/len(test_docs)*100))
    print('Took {:.6f} seconds'.format(time.clock()-start))

if __name__ == '__main__':
    main()
