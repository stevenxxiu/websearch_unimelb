
import itertools
import random

class ClassifData:
    def __init__(self, class_to_doc):
        self.class_to_docs = dict((key, set(val)) for key, val in class_to_doc.items())
        self.docs = set.union(*self.class_to_docs.values())
        self.doc_to_class = {}
        for doc_class, docs in self.class_to_docs:
            for doc in docs:
                self.doc_to_class[doc] = doc_class

    def get_doc_class(self, docid):
        return self.doc_to_class[docid]

    def get_class_docs(self, doc_class):
        return self.class_to_docs[doc_class]

    def get_class_complement_docs(self, doc_class, docs):
        return set(docs) - self.class_to_docs[doc_class]

    def get_train_test(self, ntrain, ntest, reproducible=True):
        if reproducible:
            random.seed(1)
        sample_docs = random.sample(self.docs, ntrain + ntest)
        test_docs = sample_docs[0:ntest]
        train_docs = sample_docs[ntest:(ntest + ntrain)]
        test_docs_dict = dict(itertools.groupby(test_docs, lambda docid_: self.get_doc_class(docid_)))
        train_docs_dict = dict(itertools.groupby(train_docs, lambda docid_: self.get_doc_class(docid_)))
        return test_docs_dict, train_docs_dict


def parse_lyrl_topics(path):
    with open(path, 'r') as sr:
        class_to_docs = {}
        for line in sr:
            doc_class, docs = line.split(' ', 1)
            docs = docs.split()
            class_to_docs[doc_class] = docs
        return ClassifData(class_to_docs)
