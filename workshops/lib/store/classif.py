
import pickle
import numpy as np
from scipy.sparse import csr_matrix, vstack

class ClassifDataStore:
    '''
    A document can belong to more than one class.
    '''

    def __init__(self, classif_data, docs_data):
        self.labels = sorted(classif_data.label_to_docs)
        self.label_indexes = dict((label, i) for i, label in enumerate(self.labels))
        # each row is a binary vector for a single document, containing 1 iff the document belongs to the class
        labels_rows = []
        for doc_id in docs_data.docs:
            doc_labels = sorted(classif_data.doc_to_labels.get(doc_id, []))
            row = np.zeros(len(doc_labels))
            col = np.array(list(self.label_indexes[label] for label in doc_labels))
            data = np.ones(len(doc_labels), dtype=np.int)
            labels_rows.append(csr_matrix((data, (row, col)), shape=(1, len(self.labels))))
        self.labels_matrix = vstack(labels_rows).tocsr()

    @staticmethod
    def load(store_path):
        with open(store_path, 'rb') as sr:
            # noinspection PyArgumentList
            return pickle.load(sr)

    def dump(self, store_path):
        with open(store_path, 'wb') as sr:
            # noinspection PyArgumentList
            pickle.dump(self, sr)


class LyrlClassifData:
    def __init__(self, label_to_docs, doc_to_labels):
        self.label_to_docs = label_to_docs
        self.doc_to_labels = doc_to_labels

    @classmethod
    def parse(cls, path):
        with open(path, 'r') as sr:
            label_to_docs = {}
            doc_to_labels = {}
            for line in sr:
                label, docs = line.split(' ', 1)
                docs = docs.split()
                label_to_docs[label] = docs
                for doc in docs:
                    doc_to_labels.setdefault(doc, [])
                    doc_to_labels[doc].append(label)
            return cls(label_to_docs, doc_to_labels)


class LyrlClassifDataStore(ClassifDataStore):
    def __init__(self, path, docs_data):
        super().__init__(LyrlClassifData.parse(path), docs_data)
