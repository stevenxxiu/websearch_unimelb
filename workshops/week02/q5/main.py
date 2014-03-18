
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

def get_term_vector(term, docs_db):
	res = {}
	for doc_entry in docs_db.find({'term': term}):
		res[doc_entry['doc_id']] = doc_entry['value']
	return res

def term_similarities(term, docs_db, distance_func, inverted_index_db):
	res = {}
	term_weights = get_term_vector(term, docs_db)
	#get all terms which co-occur with term
	cooccur_terms = set()
	doc_ids = inverted_index_db.find_one({'term': term})['doc_ids']
	for doc_id in doc_ids:
		cooccur_terms.update(weight_entry['term'] for weight_entry in docs_db.find({'doc_id': doc_id}))
	cooccur_terms.remove(term)
	for cooccur_term in cooccur_terms:
		res[cooccur_term] = distance_func(term_weights, get_term_vector(cooccur_term, docs_db))
	return res

def term_similarities_sorted(term, docs_db, distance_func, inverted_index_db):
	return sorted(term_similarities(term, docs_db, distance_func, inverted_index_db).items(), key=lambda t: (-t[1], t[0]))

def main():
	client = pymongo.MongoClient()
	tfidf_db = client['websearch_workshops']['week02']['tfidf']
	inverted_index_db = client['websearch_workshops']['week02']['inverted_index']
	for term in ['socc', 'jaguar', 'najibullah']:
		start=time.clock()
		query_res = term_similarities_sorted(term, tfidf_db, cosine_similarity, inverted_index_db)
		print('similar terms to {}'.format(term))
		print('{:<50}{:}'.format('term', 'score'))
		for doc_id, score in query_res[:15]:
			print('{:<50}{:}'.format(doc_id, score))
		print('Took {:.6f} seconds'.format(time.clock()-start))
		print()

if __name__ == '__main__':
	main()
