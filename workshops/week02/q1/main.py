
import time
import pymongo
from workshops.lib.weights import cosine_similarity

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
