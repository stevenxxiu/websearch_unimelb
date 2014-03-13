
import sys
sys.path.append('../lib')
import math
import time
import pymongo
from collections import Counter

def parse_query(query):
	'''
	stemming is not done
	'''
	return Counter(query.split())

def get_query_tf_idf(query, idfs):
	res = {}
	for term, term_count in query.items():
		tf = math.log(1 + term_count)
		res[term] = tf*idfs[term]
	return res

def cosine_similarity(weight_dict_1, weight_dict_2):
	'''
	assumes that both weight_dict_1 and weight_dict_2 are normalized
	'''
	score = 0
	for term in set(weight_dict_1.keys()).intersection(weight_dict_2.keys()):
		score += weight_dict_1[term]*weight_dict_2[term]
	return score

def query_similarities(query, db_collection, distance_func, idfs):
	res = {}
	query_weights = get_query_tf_idf(parse_query(query), idfs)
	for doc in db_collection.find():
		weights = doc['weights']
		res[doc['doc_id']] = distance_func(query_weights, weights)
	return res

def query_ranked_similarities(query, db_collection, distance_func, idfs):
	return sorted(query_similarities(query, db_collection, distance_func, idfs).items(), key=lambda t: (-t[1], t[0]))

def main():
	start=time.clock()
	client = pymongo.MongoClient()
	collection = client['websearch_workshops']['week02_tfidf_docs']
	idfs = client['websearch_workshops']['week02_idf_terms']
	query_res = query_ranked_similarities('jaguar car race', collection, cosine_similarity, idfs.find_one()['tfidf'])
	print('{:<50}{:}'.format('document id', 'score'))
	for doc_id, score in query_res:
		print('{:<50}{:}'.format(doc_id, score))
	print('Took {:.6f} seconds'.format(time.clock()-start))

if __name__ == '__main__':
	main()
