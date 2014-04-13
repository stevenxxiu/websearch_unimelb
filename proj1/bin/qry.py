
import os
import argparse
import numpy as np
from scipy.sparse import csr_matrix, csc_matrix, lil_matrix
from collections import Counter
from proj1.lib.store import WikiDataStore, ApacheDataStore
from proj1.lib.features import get_tf, get_tf_idf
from proj1.lib.weights import l2_norm_sparse, pivoted_length_norm

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


class RocchioForum:
    def __init__(self, wiki_data, apache_data):
        self.wiki_data = wiki_data
        self.apache_data = apache_data
        # term counts for each forum
        sub_forums_freqs = {}
        for forum_name, docs in apache_data.forum_to_docs.items():
            # get doc indexes
            doc_indexes = list(apache_data.doc_indexes[doc] for doc in docs)
            sub_forums_freqs[forum_name] = apache_data.freq_matrix[doc_indexes,:].sum(axis=0)
        self.sub_forums_freqs = sub_forums_freqs
        # wiki raw term frequencies
        self.wiki_freqs = wiki_data.freq_matrix.sum(axis=0)
        # term index map
        self.wiki_to_apache_term_indexes = {}
        for term, i in wiki_data.term_indexes.items():
            if term in apache_data.term_indexes:
                self.wiki_to_apache_term_indexes[i] = apache_data.term_indexes[term]

    def apache_to_wiki_freqs(self, X):
        '''
        convert apache frequencies to wiki frequencies
        '''
        res = lil_matrix((X.shape[0], len(self.wiki_data.terms)))
        i1, i2 = zip(*self.wiki_to_apache_term_indexes.items())
        res[:,i1] = X[:,i2]
        return res.tocsr()

    def get_query_weights(self, query_vect, post_id, alpha, beta, gamma, k):
        res = np.zeros((query_vect.shape[0], 1))
        # post weights
        res += beta * get_tf(self.apache_to_wiki_freqs(self.apache_data.freq_matrix[self.apache_data.doc_indexes[post_id]])).T
        # differentiating forum weights
        sub_forum_freqs = self.sub_forums_freqs[self.apache_data.doc_to_forum[post_id]]
        res += gamma * (
            get_tf(self.apache_to_wiki_freqs(sub_forum_freqs/sub_forum_freqs.shape[1])).T -
            get_tf(self.wiki_freqs/self.wiki_data.freq_matrix.shape[1]).T
        )
        # take top k terms
        if k is not None:
            res_top = csc_matrix((query_vect.shape[0], 1))
            top_indices = np.argsort(-np.array(res.T)[0])[:k]
            print(list(self.wiki_data.terms[i] for i in top_indices))
            res_top[top_indices,:] = res[top_indices,:]
            res = res_top
        # query weights
        res = res + alpha * get_tf(query_vect)
        return res


def query_similarities(query_vect, include_terms, X, dataset):
    # find the rows we include in the matrix
    # explicit iteration for faster results
    inc_doc_ids = set()
    for i in query_vect.nonzero()[0]:
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
    r_sparse = csc_matrix((X.shape[0], 1))
    r_sparse[inc_doc_indexes,] = r
    return r_sparse

def main():
    arg_parser=argparse.ArgumentParser(description='Run a query on the wiki.')
    arg_parser.add_argument('queries_path', type=str)
    arg_parser.add_argument('num_results', type=int)
    arg_parser.add_argument('db_path', type=str)
    arg_parser.add_argument('--include_all', action='store_true', default=False)
    arg_parser.add_argument('--pivot_slope', type=float, default=None)
    arg_parser.add_argument('--apache_postid', type=str, default=None)
    arg_parser.add_argument('--apache_rocchio', type=lambda s: (float(s.split(',')[0]), float(s.split(',')[1]), float(s.split(',')[2]), int(s.split(',')[3])), default=None)
    args=arg_parser.parse_args()

    wiki_store = WikiDataStore.load(os.path.join(args.db_path, 'wiki.db'))
    apache_store = ApacheDataStore.load(os.path.join(args.db_path, 'apache.db'))

    X = get_tf_idf(wiki_store.freq_matrix)

    if args.pivot_slope is not None:
        X = pivoted_length_norm(X, args.pivot_slope, wiki_store)
    else:
        X = l2_norm_sparse(X)

    if args.apache_rocchio is not None:
        rocchio_forum = RocchioForum(wiki_store, apache_store)
    else:
        rocchio_forum = None

    with open(args.queries_path, 'r', encoding='utf-8') as sr:
        for line in sr:
            line = line.strip()
            query_terms = parse_query(line)
            query_vect = get_query_vect(query_terms, wiki_store)
            if args.apache_rocchio is not None:
                alpha, beta, gamma, k = args.apache_rocchio
                query_vect = rocchio_forum.get_query_weights(query_vect, args.apache_postid, alpha, beta, gamma, k)
                pass
            else:
                query_vect = get_tf(query_vect)
            if args.include_all:
                include_terms = query_terms
            else:
                include_terms = None
            query_res = query_similarities(query_vect, include_terms, X, wiki_store)
            print('>> {}'.format(line))
            print('{:<50}{:}'.format('document id', 'score'))
            for i in query_res.indices[np.argsort(-query_res.data)][:args.num_results]:
                doc_id = wiki_store.docs[i]
                print('{:<50}{:.6f}'.format(doc_id, query_res[i].toarray()[0,0]))
            print()

if __name__ == '__main__':
    main()
