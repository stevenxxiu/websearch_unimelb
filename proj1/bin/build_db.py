
import os
import glob
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

def store_dataset(name, dataset):
    idfs = get_idfs(dataset)
    client = pymongo.MongoClient()

    tfidf = client['websearch_proj1'][name]['tfidf']
    tfidf.ensure_index('doc_id', unique=True)
    for doc_id in dataset.get_docs():
        weights = get_doc_tf_idf(doc_id, idfs, dataset)
        try:
            # use a list as mongodb doesn't allow keys containing '.'
            tfidf.insert({'doc_id': doc_id, 'weights': list(weights.items())})
        except pymongo.errors.DuplicateKeyError:
            pass

    idf = client['websearch_proj1'][name]['idf']
    idf.ensure_index('term', unique=True)
    for term, value in idfs.items():
        try:
            idf.insert({'term': term, 'value': value})
        except pymongo.errors.DuplicateKeyError:
            pass

    inverted_index = client['websearch_proj1'][name]['inverted_index']
    inverted_index.ensure_index('term', unique=True)
    for term, doc_ids in get_inverted_index(dataset).items():
        try:
            inverted_index.insert({'term': term, 'doc_ids': doc_ids})
        except pymongo.errors.DuplicateKeyError:
            pass

def build_wiki_db(wikipath):
    wiki_data = TitleTermData.load(wikipath)
    store_dataset('wiki', wiki_data)

def build_apache_db(apachepath):
    datasets = []
    client = pymongo.MongoClient()
    forum_docs_db = client['websearch_proj1']['apache']['form_docs']
    forum_docs_db.ensure_index('name', unique=True)
    forum_docs_db.ensure_index('doc_ids', unique=True)
    for forum_name in os.listdir(apachepath):
        for file_name in os.listdir(os.path.join(apachepath, forum_name)):
            if file_name.endswith('.txt'):
                dataset = TitleTermData.load(os.path.join(apachepath, forum_name, file_name))
                datasets.append(dataset)
                forum_docs_db.insert({'name': forum_name, 'doc_ids': list(dataset.get_docs().keys())})
    apache_data = TitleTermData.merge(datasets)
    store_dataset('apache', apache_data)

def main():
    arg_parser=argparse.ArgumentParser(description='Build the wiki tf-idf db.')
    arg_parser.add_argument('wikipath', type=str)
    arg_parser.add_argument('apachepath', type=str)
    args=arg_parser.parse_args()
    # we use separate collections for wikipedia and the apache forum, as the document lengths and term occurances likely differ
    build_wiki_db(args.wikipath)
    build_apache_db(args.apachepath)

if __name__ == '__main__':
    main()
