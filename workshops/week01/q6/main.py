import sys

from workshops.lib import coll

sys.path.append('../lib')
import math
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
	#l2 length
	term_vector_length = math.sqrt(sum(term_count**2 for term_count in doc.terms.values()))
	for term, term_count in doc.terms.items():
		term_weight = math.log(1 + (term_count/term_vector_length))
		res[term] = term_weight*idfs[term]
	return res

def cosine_similarity(weight_dict_1, weight_dict_2):
	'''
	assumes that both weight_dict_1 and weight_dict_2 are normalized
	'''
	score = 0
	for term in set(weight_dict_1.keys()).intersection(weight_dict_2.keys()):
		score += weight_dict_1[term]*weight_dict_2[term]
	return score

def doc_similarity(doc_id_1, doc_id_2, distance_func, idfs, coll_data):
	return distance_func(
		get_doc_tf_idf(doc_id_1, idfs, coll_data),
		get_doc_tf_idf(doc_id_2, idfs, coll_data)
	)

def doc_similarities(doc_id, distance_func, idfs, coll_data):
	res = {}
	for doc_id_other in coll_data.get_docs():
		if doc_id != doc_id_other:
			res[doc_id_other] = doc_similarity(doc_id, doc_id_other, distance_func, idfs, coll_data)
	return res

def doc_ranked_similarities(doc_id, distance_func, idfs, coll_data):
	return sorted(doc_similarities(doc_id, distance_func, idfs, coll_data).items(), key=lambda t: (-t[1], t[0]))

def main():
	coll_data = coll.parse_lyrl_coll('../../../../data/lyrl_tokens_30k.dat')
	idfs = get_inverse_doc_freqs(coll_data)
	print('{:<50}{:}'.format('document id', 'score'))
	for doc_id, score in doc_ranked_similarities('26413', cosine_similarity, idfs, coll_data):
		print('{:<50}{:}'.format(doc_id, score))

if __name__ == '__main__':
	main()
