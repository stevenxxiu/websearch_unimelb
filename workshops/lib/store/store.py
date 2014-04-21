
import pickle
import numpy as np
from scipy.sparse import csr_matrix, vstack
from workshops.lib.store import coll

def get_inverted_index(dataset):
    res = {}
    for doc_id in dataset.get_docs():
        doc = dataset.get_doc(doc_id)
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
        self.term_indexes = dict((term, i) for i, term in enumerate(self.terms))
        self.docs = sorted(dataset.get_docs().keys())
        self.doc_indexes = dict((doc, i) for i, doc in enumerate(self.docs))
        # csr frequency matrix with documents as rows
        # we do not use a csc matrix as constructing a csr matrix is easier,
        # and term spaces are used more often than document spaces
        freq_rows = []
        for doc_id in self.docs:
            # make sure this is deterministic
            term_freqs = list(dataset.get_doc(doc_id).terms.items())
            row = np.zeros(len(term_freqs))
            col = np.array(list(self.term_indexes[term] for term, freq in term_freqs))
            data = np.array(list(freq for term, freq in term_freqs))
            freq_rows.append(csr_matrix((data, (row, col)), shape=(1, len(terms))))
        self.freq_matrix = vstack(freq_rows).tocsr()
        # inverted index
        self.inverted_index = get_inverted_index(dataset)

    @staticmethod
    def load(store_path):
        with open(store_path, 'rb') as sr:
            return pickle.load(sr)

    def dump(self, store_path):
        with open(store_path, 'wb') as sr:
            pickle.dump(self, sr)


class CollDataStore(DataStore):
    def __init__(self, path):
        super().__init__(coll.parse_lyrl_coll(path))

