
import math
import argparse
import pymongo
import pymongo.errors
from collections import Counter
from proj1.lib.weights import cosine_similarity, l2_norm, l2_dist, PivotedLengthNorm, WeightDict

def parse_query(query):
    '''
    stemming is not done
    '''
    return Counter(query.split())

def get_tf(query_freqs):
    res = WeightDict()
    for term, count in query_freqs.items():
        res[term] = math.log(1+count)
    return res


class RocchioForum:
    def __init__(self):
        client = pymongo.MongoClient()
        # forum raw term frequencies
        sub_forums_freqs = {}
        freqs_db = client['websearch_proj1']['apache']['freq']
        for sub_forum in client['websearch_proj1']['apache']['forum_docs'].find():
            sub_forum_freqs = WeightDict()
            for doc in freqs_db.find({'doc_id': {'$in': sub_forum['doc_ids']}}):
                sub_forum_freqs += WeightDict(dict(doc['freqs']))
            sub_forums_freqs[sub_forum['name']] = sub_forum_freqs
        self.sub_forums_freqs = sub_forums_freqs
        # wiki raw term frequencies
        wiki_freqs = WeightDict()
        freqs_db = client['websearch_proj1']['wiki']['freq']
        for doc in freqs_db.find():
            wiki_freqs += WeightDict(dict(doc['freqs']))
        self.wiki_freqs = wiki_freqs

    def get_query_weights(self, query_weight_dict, post_id, alpha, beta, gamma, k):
        res = WeightDict()
        client = pymongo.MongoClient()
        forum_docs_db = client['websearch_proj1']['apache']['forum_docs']
        sub_forum = forum_docs_db.find_one({'doc_ids': post_id})
        weights_db = client['websearch_proj1']['apache']['freq']
        # post weights
        res += beta * get_tf(dict(weights_db.find_one({'doc_id': post_id})['freqs']))
        # differentiating forum weights
        res += gamma * \
            get_tf(self.sub_forums_freqs[sub_forum['name']]/client['websearch_proj1']['apache']['freq'].count()) - \
            get_tf(self.wiki_freqs/client['websearch_proj1']['wiki']['freq'].count())
        # take top k terms
        res = WeightDict(dict(sorted(res.items(), key=lambda x: (-x[1], x[0]))[:k]))
        # query weights
        res += alpha * get_tf(query_weight_dict)
        return res


def query_similarities(query_weight_dict, distance_func, norm_func, include_terms, docs_db, inverted_index_db):
    res = {}
    docs = inverted_index_db.find({'term': {'$in': list(query_weight_dict.keys())}})
    # explicit iteration for faster results
    doc_ids = set()
    for doc in docs:
        doc_ids.update(doc['doc_ids'])
    # make sure all terms in include_terms are included in the set of documents
    if include_terms is not None:
        docs_include = inverted_index_db.find({'term': {'$in': include_terms}})
        for doc in docs_include:
            doc_ids.intersection_update(doc['doc_ids'])
    # calculate similarities between the query and all documents
    for doc_id in doc_ids:
        doc = docs_db.find_one({'doc_id': doc_id})
        weights = norm_func(dict(doc['weights']))
        res[doc_id] = distance_func(query_weight_dict, weights)
    return res

def query_similarities_sorted(sims):
    return sorted(sims.items(), key=lambda t: (-t[1], t[0]))

def main():
    arg_parser=argparse.ArgumentParser(description='Run a query on the wiki.')
    arg_parser.add_argument('queries_path', type=str)
    arg_parser.add_argument('num_results', type=int)
    arg_parser.add_argument('--include_all', action='store_true', default=False)
    arg_parser.add_argument('--pivot_slope', type=float, default=None)
    arg_parser.add_argument('--apache_postid', type=str, default=None)
    arg_parser.add_argument('--apache_rocchio', type=lambda s: (float(s.split(',')[0]), float(s.split(',')[1]), float(s.split(',')[2]), int(s.split(',')[3])), default=None)
    args=arg_parser.parse_args()

    client = pymongo.MongoClient()
    tfidf_db = client['websearch_proj1']['wiki']['tfidf']
    inverted_index = client['websearch_proj1']['wiki']['inverted_index']

    if args.pivot_slope is not None:
        pl_norm = PivotedLengthNorm(l2_dist, (dict(doc['weights']) for doc in tfidf_db.find()))
        norm_func = lambda w: pl_norm.norm(w, args.pivot_slope)
    else:
        norm_func = l2_norm

    if args.apache_rocchio is not None:
        rocchio_forum = RocchioForum()
    else:
        rocchio_forum = None

    with open(args.queries_path, 'r', encoding='utf-8') as sr:
        for line in sr:
            line = line.strip()
            query_weights = parse_query(line)
            query_terms = list(query_weights.keys())
            if args.apache_rocchio is not None:
                alpha, beta, gamma, k = args.apache_rocchio
                query_weights = rocchio_forum.get_query_weights(query_weights, args.apache_postid, alpha, beta, gamma, k)
            else:
                query_weights = get_tf(query_weights)
            if args.include_all:
                include_terms = query_terms
            else:
                include_terms = None
            query_res = query_similarities_sorted(
                query_similarities(query_weights, cosine_similarity, norm_func, include_terms, tfidf_db, inverted_index)
            )
            print('>> {}'.format(line))
            print('{:<50}{:}'.format('document id', 'score'))
            for doc_id, score in query_res[:args.num_results]:
                print('{:<50}{:.6f}'.format(doc_id, score))
            print()

if __name__ == '__main__':
    main()
