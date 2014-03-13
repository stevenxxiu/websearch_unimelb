
import sys
sys.path.append('../')
import coll
from collections import Counter

def get_doc_freqs(coll_data):
	dfs = Counter()
	for doc_id in coll_data.get_docs():
		doc = coll_data.get_doc(doc_id)
		dfs.update(dict(zip(doc.terms.keys(), [1]*len(doc.terms))))
	return dfs

def main():
	coll_data = coll.parse_lyrl_coll('../../../../data/lyrl_tokens_30k.dat')
	dfs_sorted = sorted(get_doc_freqs(coll_data).items(), key=lambda t: (-t[1], t[0]))
	print('{:<50}{:}'.format('TERM', 'DOC_FREQ'))
	for term, freqs in dfs_sorted:
		print('{:<50}{:}'.format(term, freqs))

if __name__ == '__main__':
	main()
