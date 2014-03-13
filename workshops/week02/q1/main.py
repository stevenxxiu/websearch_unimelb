
import sys
sys.path.append('../lib')
import pymongo

def cosine_similarity(weight_dict_1, weight_dict_2):
	'''
	assumes that both weight_dict_1 and weight_dict_2 are normalized
	'''
	score = 0
	for term in set(weight_dict_1.keys()).intersection(weight_dict_2.keys()):
		score += weight_dict_1[term]*weight_dict_2[term]
	return score

def doc_similarity(doc_id_1, doc_id_2, distance_func, db_collection):
	return distance_func(
		db_collection.find_one({'doc_id': doc_id_1})['weights'],
		db_collection.find_one({'doc_id': doc_id_2})['weights']
	)

def main():
	client = pymongo.MongoClient()
	collection = client['websearch_workshops']['week02_tfidf_index']
	print(doc_similarity('26152', '26159', cosine_similarity, collection))
	print(doc_similarity('26152', '26413', cosine_similarity, collection))

if __name__ == '__main__':
	main()
