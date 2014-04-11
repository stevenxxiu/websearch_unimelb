
import math
import argparse
import pymongo
import pymongo.errors
from collections import Counter
from proj1.lib.weights import cosine_similarity

def parse_query(query):
    '''
    stemming is not done
    '''
    return Counter(query.split())

def get_query_weights(query_terms):
    res = {}
    for term, count in query_terms.items():
        res[term] = math.log(1+count)
    return res

def query_similarities(query_weight_dict, docs_db, distance_func, inverted_index_db):
    res = {}
    doc_ids = set()
    for doc_ids_entry in inverted_index_db.find({'$or': [{'term': query_term} for query_term in query_weight_dict]}, ['doc_ids']):
        doc_ids.update(doc_ids_entry['doc_ids'])
    for doc_id in doc_ids:
        doc = docs_db.find_one({'doc_id': doc_id})
        weights = dict(doc['weights'])
        res[doc_id] = distance_func(query_weight_dict, weights)
    return res

def query_similarities_sorted(query_weight_dict, docs_db, distance_func, inverted_index_db):
    return sorted(query_similarities(query_weight_dict, docs_db, distance_func, inverted_index_db).items(), key=lambda t: (-t[1], t[0]))

def main():
    arg_parser=argparse.ArgumentParser(description='Build the wiki tf-idf db.')
    arg_parser.add_argument('queries_path', type=str)
    arg_parser.add_argument('num_results', type=int)
    args=arg_parser.parse_args()
    
    client = pymongo.MongoClient()
    tfidf_db = client['websearch_proj1']['wiki']['tfidf']
    inverted_index = client['websearch_proj1']['wiki']['inverted_index']

    with open(args.queries_path, 'r', encoding='utf-8') as sr:
        for line in sr:
            line = line.strip()
            query_weights = get_query_weights(parse_query(line))
            query_res = query_similarities_sorted(query_weights, tfidf_db, cosine_similarity, inverted_index)
            print('>> {}'.format(line))
            print('{:<50}{:}'.format('document id', 'score'))
            for doc_id, score in query_res[:args.num_results]:
                print('{:<50}{:.6f}'.format(doc_id, score))
            print()

if __name__ == '__main__':
    main()
