
from workshops.lib import coll
from workshops.lib.features import get_idfs, get_doc_tf_idf_raw

def main():
	coll_data = coll.parse_lyrl_coll('../../../../data/lyrl_tokens_30k.dat')
	idfs = get_idfs(coll_data)
	for doc_id in coll_data.get_docs():
		print(doc_id, get_doc_tf_idf_raw(doc_id, idfs, coll_data))

if __name__ == '__main__':
	main()
