
import numpy as np
import matplotlib.pyplot as plt
from workshops.lib.store import coll

def get_docinfo(coll_data):
	num_terms_cum=[]
	terms = set()
	for doc_id in coll_data.get_docs():
		terms.update(coll_data.get_doc(doc_id).terms.keys())
		num_terms_cum.append(len(terms))
	plt.title('cumulative growth')
	plt.bar(np.arange(coll_data.get_num_docs()), np.array(num_terms_cum), align='center', width=0.8)
	plt.show()
	plt.title('growth')
	plt.bar(np.arange(coll_data.get_num_docs()-1), np.diff(num_terms_cum), align='center', width=0.8)
	plt.show()

def main():
	coll_data = coll.parse_lyrl_coll('../../../../data/lyrl_tokens_30k.dat')
	get_docinfo(coll_data)

if __name__ == '__main__':
	main()
