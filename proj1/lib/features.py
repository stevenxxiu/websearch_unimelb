
import math
from collections import Counter

def get_dfs(wiki_data):
	dfs = Counter()
	for doc_id in wiki_data.get_docs():
		doc = wiki_data.get_doc(doc_id)
		dfs.update(dict(zip(doc.terms.keys(), [1]*len(doc.terms))))
	return dfs

def get_idfs(wiki_data):
	res = {}
	dfs = get_dfs(wiki_data)
	num_docs = wiki_data.get_num_docs()
	for term, df in dfs.items():
		res[term] = math.log(num_docs) - math.log(df)
	return res

def get_doc_tf_idf(doc_id, idfs, wiki_data):
	res = {}
	doc = wiki_data.get_doc(doc_id)
	for term, term_count in doc.terms.items():
		tf = math.log(1 + term_count)
		res[term] = tf*idfs[term]
	#l2 length
	term_vector_length = math.sqrt(sum(term_weight**2 for term_weight in res.values()))
	for term, term_weight in res.items():
		res[term] = term_weight/term_vector_length
	return res
