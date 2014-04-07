
import pymongo
import pymongo.errors
from workshops.lib import coll
from workshops.lib.features import get_idfs, get_doc_tf_idf

def get_inverted_index(coll_data):
    res = {}
    for doc_id in coll_data.get_docs():
        doc = coll_data.get_doc(doc_id)
        for term in doc.terms:
            if term not in res:
                res[term] = []
            res[term].append(doc_id)
    return res

def main():
    coll_data = coll.parse_lyrl_coll('../../../data/lyrl_tokens_30k.dat')
    idfs = get_idfs(coll_data)
    client = pymongo.MongoClient()

    tfidf = client['websearch_workshops']['lyrl']['tfidf']
    tfidf.ensure_index('doc_id', unique=True)
    for doc_id in coll_data.get_docs():
        weights = get_doc_tf_idf(doc_id, idfs, coll_data)
        try:
            tfidf.insert({'doc_id': doc_id, 'weights': weights})
        except pymongo.errors.DuplicateKeyError:
            pass

    idf = client['websearch_workshops']['lyrl']['idf']
    idf.ensure_index('term', unique=True)
    for term, value in idfs.items():
        try:
            idf.insert({'term': term, 'value': value})
        except pymongo.errors.DuplicateKeyError:
            pass

    inverted_index = client['websearch_workshops']['lyrl']['inverted_index']
    inverted_index.ensure_index('term', unique=True)
    for term, doc_ids in get_inverted_index(coll_data).items():
        try:
            inverted_index.insert({'term': term, 'doc_ids': doc_ids})
        except pymongo.errors.DuplicateKeyError:
            pass

if __name__ == '__main__':
    main()
