
import os
import argparse
import numpy as np
from scipy.sparse import csr_matrix, diags
from collections import Counter
from proj1.lib.store import WikiDataStore, ApacheDataStore
from proj1.lib.features import get_tf, get_tf_idf
from proj1.lib.weights import l2_norm_sparse, PivotedLengthNorm

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
    return csr_matrix((data, (row, col)), shape=(1, len(term_indexes)))


# class RocchioForum:
#     def __init__(self):
#         client = pymongo.MongoClient()
#         # forum raw term frequencies
#         sub_forums_freqs = {}
#         freqs_db = client['websearch_proj1']['apache']['freq']
#         for sub_forum in client['websearch_proj1']['apache']['forum_docs'].find():
#             sub_forum_freqs = WeightDict()
#             for doc in freqs_db.find({'doc_id': {'$in': sub_forum['doc_ids']}}):
#                 sub_forum_freqs += WeightDict(dict(doc['freqs']))
#             sub_forums_freqs[sub_forum['name']] = sub_forum_freqs
#         self.sub_forums_freqs = sub_forums_freqs
#         # wiki raw term frequencies
#         wiki_freqs = WeightDict()
#         freqs_db = client['websearch_proj1']['wiki']['freq']
#         for doc in freqs_db.find():
#             wiki_freqs += WeightDict(dict(doc['freqs']))
#         self.wiki_freqs = wiki_freqs
#
#     def get_query_weights(self, query_weight_dict, post_id, alpha, beta, gamma, k):
#         res = WeightDict()
#         client = pymongo.MongoClient()
#         forum_docs_db = client['websearch_proj1']['apache']['forum_docs']
#         sub_forum = forum_docs_db.find_one({'doc_ids': post_id})
#         weights_db = client['websearch_proj1']['apache']['freq']
#         # post weights
#         res += beta * get_tf(dict(weights_db.find_one({'doc_id': post_id})['freqs']))
#         # differentiating forum weights
#         res += gamma * \
#             get_tf(self.sub_forums_freqs[sub_forum['name']]/client['websearch_proj1']['apache']['freq'].count()) - \
#             get_tf(self.wiki_freqs/client['websearch_proj1']['wiki']['freq'].count())
#         # take top k terms
#         res = WeightDict(dict(sorted(res.items(), key=lambda x: (-x[1], x[0]))[:k]))
#         # query weights
#         res += alpha * get_tf(query_weight_dict)
#         return res


def query_similarities(query_vect, include_terms, X, dataset):
    # find the rows we include in the matrix
    # explicit iteration for faster results
    inc_doc_ids = set()
    for i in query_vect.nonzero()[1]:
        inc_doc_ids.update(dataset.inverted_index[dataset.terms[i]])
    if include_terms is not None:
        # make sure all terms in include_terms are included in the set of documents
        for term in include_terms:
            inc_doc_ids.intersection_update(dataset.inverted_index[term])
    inc_doc_indexes = list(dataset.doc_indexes[doc_id] for doc_id in inc_doc_ids)
    print(len(inc_doc_indexes))
    #XXX fix the result indices
    Y = X[inc_doc_indexes,]
    return Y*query_vect.T

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
        # XXX
        # pl_norm = PivotedLengthNorm(l2_dist, (dict(doc['weights']) for doc in tfidf_db.find()))
        # norm_func = lambda w: pl_norm.norm(w, args.pivot_slope)
        pass
    else:
        X = l2_norm_sparse(X)

    # XXX
    # if args.apache_rocchio is not None:
    #     rocchio_forum = RocchioForum()
    # else:
    #     rocchio_forum = None

    with open(args.queries_path, 'r', encoding='utf-8') as sr:
        for line in sr:
            line = line.strip()
            query_terms = parse_query(line)
            query_vect = get_query_vect(query_terms, wiki_store)
            # XXX
            if args.apache_rocchio is not None:
                # alpha, beta, gamma, k = args.apache_rocchio
                # query_vect = rocchio_forum.get_query_weights(query_vect, args.apache_postid, alpha, beta, gamma, k)
                pass
            else:
                query_vect = get_tf(query_vect)
            if args.include_all:
                include_terms = query_terms
            else:
                include_terms = None
            query_res = query_similarities(query_vect, include_terms, X, wiki_store)
            print(sorted(query_res.data, reverse=True))
            # XXX
            # print('>> {}'.format(line))
            # print('{:<50}{:}'.format('document id', 'score'))
            # for doc_id, score in query_res[:args.num_results]:
            #     print('{:<50}{:.6f}'.format(doc_id, score))
            # print()

if __name__ == '__main__':
    main()
