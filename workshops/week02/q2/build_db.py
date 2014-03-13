
import sys
sys.path.append('../lib')
import math
import pymongo
import coll
from collections import Counter

def get_doc_freqs(coll_data):
	dfs = Counter()
	for doc_id in coll_data.get_docs():
		doc = coll_data.get_doc(doc_id)
		dfs.update(dict(zip(doc.terms.keys(), [1]*len(doc.terms))))
	return dfs

def get_inverse_doc_freqs(coll_data):
	res = {}
	dfs = get_doc_freqs(coll_data)
	num_docs = coll_data.get_num_docs()
	for term, df in dfs.items():
		res[term] = math.log(num_docs) - math.log(df)
	return res

def get_doc_tf_idf(doc_id, idfs, coll_data):
	res = {}
	doc = coll_data.get_doc(doc_id)
	for term, term_count in doc.terms.items():
		tf = math.log(1 + term_count)
		res[term] = tf*idfs[term]
	#l2 length
	term_vector_length = math.sqrt(sum(term_weight**2 for term_weight in res.values()))
	for term, term_weight in res.items():
		res[term] = term_weight/term_vector_length
	return res

def main():
	coll_data = coll.parse_lyrl_coll('../../../../data/lyrl_tokens_30k.dat')
	idfs = get_inverse_doc_freqs(coll_data)
	client = pymongo.MongoClient()
	collection = client['websearch_workshops']['week02_tfidf_docs']
	for doc_id in coll_data.get_docs():
		collection.insert({'doc_id': doc_id, 'weights': get_doc_tf_idf(doc_id, idfs, coll_data)})
	collection = client['websearch_workshops']['week02_idf_terms']
	collection.insert({'tfidf': idfs})

if __name__ == '__main__':
	main()
