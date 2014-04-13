
from collections import Counter

class TitleTermDoc:
    def __init__(self, doc_id, terms):
        self.doc_id = doc_id
        self.terms = Counter(terms)

class TitleTermData:
    def __init__(self, docs):
        self.docs = docs

    @classmethod
    def load(cls, path):
        docs = {}
        with open(path, 'r', encoding='utf-8') as sr:
            for i, line in enumerate(sr):
                title, terms = line.split(maxsplit=1)
                terms = terms.split()
                docs[title] = TitleTermDoc(title, terms)
        return cls(docs)

    def get_docs(self):
        return self.docs

    def get_doc(self, docid):
        return self.docs[docid]

    def get_num_docs(self):
        return len(self.docs)
