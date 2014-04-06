
import time
import pymongo

def cosine_similarity(weight_dict_1, weight_dict_2):
	'''
	assumes that both weight_dict_1 and weight_dict_2 are normalized
	'''
	score = 0
	for term in set(weight_dict_1.keys()).intersection(weight_dict_2.keys()):
		score += weight_dict_1[term]*weight_dict_2[term]
	return score

def doc_similarity(doc_id_1, doc_id_2, docs_db, distance_func):
	return distance_func(
		docs_db.find_one({'doc_id': doc_id_1})['weights'],
		docs_db.find_one({'doc_id': doc_id_2})['weights']
	)

def main():
	start=time.clock()
	client = pymongo.MongoClient()
	collection = client['websearch_workshops']['lyrl']['tfidf']
	print(doc_similarity('26151', '26152', collection, cosine_similarity))
	print('Took {:.6f} seconds'.format(time.clock()-start))

if __name__ == '__main__':
	main()
