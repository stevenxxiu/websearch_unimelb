
from workshops.lib import coll
from workshops.lib.weights import cosine_similarity
from workshops.lib.features import get_idfs, get_doc_tf_idf

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
	idfs = get_idfs(coll_data)
	print('{:<50}{:}'.format('document id', 'score'))
	for doc_id, score in doc_ranked_similarities('26413', cosine_similarity, idfs, coll_data):
		print('{:<50}{:}'.format(doc_id, score))

if __name__ == '__main__':
	main()
