
from collections import Counter

class WikiDoc:
    def __init__(self, doc_id, terms):
        self.doc_id = doc_id
        self.terms = Counter(terms)


class WikiData:
    def __init__(self, docs):
        self.docs = docs

    @classmethod
    def load(cls, path):
        docs = {}
        with open(path, 'r') as sr:
            for line in sr:
                doc_id, doc = line.split(maxsplit=1)
                terms = doc.split()
                docs[doc_id] = WikiDoc(doc_id, terms)
        return cls(docs)

    def get_docs(self):
        return self.docs

    def get_doc(self, docid):
        return self.docs[docid]
