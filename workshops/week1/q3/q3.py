
import math
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
	for term, term_count in coll_data.get_doc(doc_id).terms.items():
		res[term] = term_count*idfs[term]
	return res

def main():
	coll_data = coll.parse_lyrl_coll('../../../../data/lyrl_tokens_30k.dat')
	idfs = get_inverse_doc_freqs(coll_data)
	for doc_id in coll_data.get_docs():
		print(doc_id, get_doc_tf_idf(doc_id, idfs, coll_data))

if __name__ == '__main__':
	main()
