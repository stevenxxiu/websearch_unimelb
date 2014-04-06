
import math
import time
import pymongo
from collections import Counter

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

def cosine_similarity(weight_dict_1, weight_dict_2):
	'''
	assumes that both weight_dict_1 and weight_dict_2 are normalized
	'''
	score = 0
	for term in set(weight_dict_1.keys()).intersection(weight_dict_2.keys()):
		score += weight_dict_1[term]*weight_dict_2[term]
	return score

def query_similarities(query_weights, docs_db, distance_func):
	res = {}
	for doc in docs_db.find():
		weights = doc['weights']
		res[doc['doc_id']] = distance_func(query_weights, weights)
	return res

def query_similarities_sorted(query, docs_db, distance_func):
	for doc_id, score in sorted(query_similarities(query, docs_db, distance_func).items(), key=lambda t: (-t[1], t[0])):
		if score==0:
			break
		yield doc_id, score

def main():
	start=time.clock()
	client = pymongo.MongoClient()
	tfidf_db = client['websearch_workshops']['lyrl']['tfidf']
	idfs_db = client['websearch_workshops']['lyrl']['idf']
	query_weights = parse_query('jaguar car race')
	query_res = query_similarities_sorted(query_weights, tfidf_db, cosine_similarity)
	print('{:<50}{:}'.format('document id', 'score'))
	for doc_id, score in query_res:
		print('{:<50}{:}'.format(doc_id, score))
	print('Took {:.6f} seconds'.format(time.clock()-start))

if __name__ == '__main__':
	main()
