
import os
import argparse
import pickle
import numpy as np
from scipy.sparse import csr_matrix, vstack
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


class DataStore:
    def __init__(self, dataset):
        terms = set()
        for doc_id, doc in dataset.get_docs().items():
            terms.update(doc.terms.keys())
        self.terms = sorted(terms)
        self.term_indexes = dict((term, i) for i, term in enumerate(terms))
        self.docs = sorted(dataset.get_docs().keys())
        self.doc_indexes = dict((doc, i) for i, doc in enumerate(self.docs))
        # csr frequency matrix with documents as rows
        # we do not use a csc matrix as constructing a csr matrix is easier,
        # and term spaces are used more often than document spaces
        freq_rows = []
        for doc_id, doc in dataset.get_docs().items():
            # make sure this is deterministic
            term_freqs = list(doc.terms.items())
            row = np.zeros(len(term_freqs))
            col = np.array(list(self.term_indexes[term] for term, freq in term_freqs))
            data = np.array(list(freq for term, freq in term_freqs))
            freq_rows.append(csr_matrix((data, (row, col)), shape=(1, len(terms))))
        self.freq_matrix = vstack(freq_rows)
        # inverted index
        self.inverted_index = get_inverted_index(dataset)


def build_wiki_db(wiki_path, store_path):
    dataset = TitleTermData.load(wiki_path)
    with open(store_path, 'wb') as sr:
        pickle.dump(DataStore(dataset), sr)

#def build_apache_db(apachepath):
#    datasets = []
#    client = pymongo.MongoClient()
#    forum_docs_db = client['websearch_proj1']['apache']['forum_docs']
#    forum_docs_db.ensure_index('name', unique=True)
#    forum_docs_db.ensure_index('doc_ids', unique=True)
#    for forum_name in os.listdir(apachepath):
#        for file_name in os.listdir(os.path.join(apachepath, forum_name)):
#            if file_name.endswith('.txt'):
#                dataset = TitleTermData.load(os.path.join(apachepath, forum_name, file_name))
#                datasets.append(dataset)
#                forum_docs_db.insert({'name': forum_name, 'doc_ids': list(dataset.get_docs().keys())})
#    apache_data = TitleTermData.merge(datasets)
#    store_dataset('apache', apache_data)

def main():
    arg_parser=argparse.ArgumentParser(description='Build the wiki tf-idf db.')
    arg_parser.add_argument('wiki_path', type=str)
    arg_parser.add_argument('apache_path', type=str)
    arg_parser.add_argument('store_path', type=str)
    args=arg_parser.parse_args()
    # we use separate collections for wikipedia and the apache forum, as the document lengths and term occurances likely differ
    build_wiki_db(args.wiki_path, os.path.join(args.store_path, 'wiki.db'))
    # build_apache_db(args.apachepath)

if __name__ == '__main__':
    main()
