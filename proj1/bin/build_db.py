
import argparse
import pymongo
import pymongo.errors
from proj1.lib.data import TitleTermData
from proj1.lib.features import get_idfs, get_doc_tf_idf

def get_inverted_index(wiki_data):
    res = {}
    for doc_id in wiki_data.get_docs():
        doc = wiki_data.get_doc(doc_id)
        for term in doc.terms:
            res.setdefault(term, [])
            res[term].append(doc_id)
    return res

def main():
    arg_parser=argparse.ArgumentParser(description='Build the wiki tf-idf db.')
    arg_parser.add_argument('wikipath', type=str)
    args=arg_parser.parse_args()
    
    wiki_data = TitleTermData.load(args.wikipath)
    idfs = get_idfs(wiki_data)
    client = pymongo.MongoClient()

    tfidf = client['websearch_proj1']['wiki']['tfidf']
    tfidf.ensure_index('doc_id', unique=True)
    for doc_id in wiki_data.get_docs():
        weights = get_doc_tf_idf(doc_id, idfs, wiki_data)
        try:
            # use a list as mongodb doesn't allow keys containing '.'
            tfidf.insert({'doc_id': doc_id, 'weights': list(weights.items())})
        except pymongo.errors.DuplicateKeyError:
            pass

    idf = client['websearch_proj1']['wiki']['idf']
    idf.ensure_index('term', unique=True)
    for term, value in idfs.items():
        try:
            idf.insert({'term': term, 'value': value})
        except pymongo.errors.DuplicateKeyError:
            pass

    inverted_index = client['websearch_proj1']['wiki']['inverted_index']
    inverted_index.ensure_index('term', unique=True)
    for term, doc_ids in get_inverted_index(wiki_data).items():
        try:
            inverted_index.insert({'term': term, 'doc_ids': doc_ids})
        except pymongo.errors.DuplicateKeyError:
            pass

if __name__ == '__main__':
    main()
