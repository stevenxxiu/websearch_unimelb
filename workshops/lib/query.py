
import numpy as np
from collections import Counter
from scipy.sparse import csr_matrix, lil_matrix

def parse_query(query):
    '''
    stemming is not done
    '''
    return query.split()

def get_query_vect(query, dataset):
    '''
    parse a query into a sparse matrix
    '''
    term_indexes = dataset.term_indexes
    # make sure this is deterministic
    term_freqs = sorted(Counter(query).items())
    row = np.zeros(len(term_freqs))
    col = np.array(list(term_indexes[term] for term, freq in term_freqs))
    data = np.array(list(freq for term, freq in term_freqs))
    return csr_matrix((data, (row, col)), shape=(1, len(term_indexes))).T

def query_similarities(query_vect, include_terms, X, dataset):
    # find the rows we include in the matrix
    # explicit iteration for faster results
    inc_doc_ids = set()
    query_non_zero = query_vect.nonzero()[0]
    if isinstance(query_non_zero, np.matrix):
        # noinspection PyUnresolvedReferences
        query_non_zero = query_non_zero.A1
    for i in query_non_zero:
        inc_doc_ids.update(dataset.inverted_index[dataset.terms[i]])
    if include_terms is not None:
        # make sure all terms in include_terms are included in the set of documents
        for term in include_terms:
            inc_doc_ids.intersection_update(dataset.inverted_index[term])
    inc_doc_indexes = list(dataset.doc_indexes[doc_id] for doc_id in inc_doc_ids)
    # use the inverted index for faster multiplication
    Y = X[inc_doc_indexes,]
    r = Y*query_vect
    # restore zero indexes, return a vector as it's better to be consistent
    r_sparse = lil_matrix((X.shape[0], 1))
    r_sparse[inc_doc_indexes,] = r
    return r_sparse
