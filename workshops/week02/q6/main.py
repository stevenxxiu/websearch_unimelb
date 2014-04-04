
import math
import time
import pymongo
from collections import Counter
from workshops.lib.weights import cosine_similarity, normalize_weights, WeightDict

def parse_query(query):
	'''
	stemming is not done
	'''
	return Counter(query.split())

def get_query_tf_idf(query, idfs_db):
	res = {}
	for term, term_count in query.items():
		tf = math.log(1 + term_count)
		idf_entry = idfs_db.find_one({'term': term})
		if idf_entry is None:
			continue
		res[term] = tf*idf_entry['value']
	return res

def query_similarities(query_weight_dict, docs_db, distance_func, inverted_index_db):
	res = {}
	doc_ids = set()
	for doc_ids_entry in inverted_index_db.find({'$or': [{'term': query_term} for query_term in query_weight_dict]}, ['doc_ids']):
		doc_ids.update(doc_ids_entry['doc_ids'])
	for doc_id in doc_ids:
		doc = docs_db.find_one({'doc_id': doc_id})
		weights = doc['weights']
		res[doc_id] = distance_func(query_weight_dict, weights)
	return res

def query_similarities_sorted(query_weight_dict, docs_db, distance_func, inverted_index_db):
	return sorted(query_similarities(query_weight_dict, docs_db, distance_func, inverted_index_db).items(), key=lambda t: (-t[1], t[0]))

def rocchio_prf(query_weight_dict, alpha, beta, result_doc_ids, docs_db):
	result_weight_dict = WeightDict()
	for doc_id in result_doc_ids:
		doc = docs_db.find_one({'doc_id': doc_id})
		result_weight_dict += doc['weights']

	return WeightDict(query_weight_dict)*alpha + result_weight_dict*(beta/len(result_doc_ids))

def main():
	start=time.clock()
	client = pymongo.MongoClient()
	tfidf_db = client['websearch_workshops']['week02']['tfidf']
	idfs_db = client['websearch_workshops']['week02']['idf']
	inverted_index = client['websearch_workshops']['week02']['inverted_index']

	#search using query
	query_weights = normalize_weights(parse_query('jaguar car race'))
	query_res = query_similarities_sorted(query_weights, tfidf_db, cosine_similarity, inverted_index)

	#get rocchio prf
	rocchio_cutoff = 5
	rocchio_doc_ids = list(doc[0] for doc in query_res[:rocchio_cutoff])
	query_weights_rocchio = rocchio_prf(query_weights, 0.5, 0.5, rocchio_doc_ids, tfidf_db)

	#search using expanded query vector
	query_res = query_similarities_sorted(query_weights_rocchio, tfidf_db, cosine_similarity, inverted_index)

	#print rocchio query results
	print('{:<50}{:}'.format('document id', 'score'))
	for doc_id, score in query_res:
		print('{:<50}{:}'.format(doc_id, score))

	print('Took {:.6f} seconds'.format(time.clock()-start))

if __name__ == '__main__':
	main()
