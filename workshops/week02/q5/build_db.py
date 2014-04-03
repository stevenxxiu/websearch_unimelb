import sys


sys.path.append('../lib')
import math
import pymongo
import pymongo.errors
from collections import Counter

def get_dfs(coll_data):
	dfs = Counter()
	for doc_id in coll_data.get_docs():
		doc = coll_data.get_doc(doc_id)
		dfs.update(dict(zip(doc.terms.keys(), [1]*len(doc.terms))))
	return dfs

def get_idfs(coll_data):
	res = {}
	dfs = get_dfs(coll_data)
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

def get_inverted_index(coll_data):
	res = {}
	for doc_id in coll_data.get_docs():
		doc = coll_data.get_doc(doc_id)
		for term in doc.terms:
			if term not in res:
				res[term] = []
			res[term].append(doc_id)
	return res

def main():
	coll_data = coll.parse_lyrl_coll('../../../../data/lyrl_tokens_30k.dat')
	idfs = get_idfs(coll_data)
	client = pymongo.MongoClient()

	tfidf = client['websearch_workshops']['week02']['tfidf']
	tfidf.ensure_index('doc_id')
	tfidf.ensure_index('term')
	for doc_id in coll_data.get_docs():
		weights = get_doc_tf_idf(doc_id, idfs, coll_data)
		if tfidf.find_one({'doc_id': doc_id}) is not None:
			continue
		tfidf.insert(list({'doc_id': doc_id, 'term': term, 'value': value} for term, value in weights.items()))

	idf = client['websearch_workshops']['week02']['idf']
	idf.ensure_index('term', unique=True)
	for term, value in idfs.items():
		try:
			idf.insert({'term': term, 'value': value})
		except pymongo.errors.DuplicateKeyError:
			pass

	inverted_index = client['websearch_workshops']['week02']['inverted_index']
	inverted_index.ensure_index('term', unique=True)
	for term, doc_ids in get_inverted_index(coll_data).items():
		try:
			inverted_index.insert({'term': term, 'doc_ids': doc_ids})
		except pymongo.errors.DuplicateKeyError:
			pass

if __name__ == '__main__':
	main()
