
from workshops.lib import coll
from workshops.lib.weights import cosine_similarity
from workshops.lib.features import get_idfs, get_doc_tf_idf

def doc_similarity(doc_id_1, doc_id_2, distance_func, idfs, coll_data):
	return distance_func(
		get_doc_tf_idf(doc_id_1, idfs, coll_data),
		get_doc_tf_idf(doc_id_2, idfs, coll_data)
	)

def main():
	coll_data = coll.parse_lyrl_coll('../../../../data/lyrl_tokens_30k.dat')
	idfs = get_idfs(coll_data)
	print(doc_similarity('26152', '26159', cosine_similarity, idfs, coll_data))
	print(doc_similarity('26152', '26413', cosine_similarity, idfs, coll_data))

if __name__ == '__main__':
	main()
