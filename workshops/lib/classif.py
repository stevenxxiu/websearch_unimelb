
from workshops.lib.weights import WeightDict

class Rocchio:
    def __init__(self, distance_func):
        self.class_mean_weights = {}
        self.distance_func = distance_func

    def train(self, train_dict, docs_db):
        mean_weights = {}
        for doc_class, doc_ids in train_dict.items():
            mean_weights[doc_class] = sum(WeightDict(docs_db.find_one({'doc_id': doc_id})['weights']) for doc_id in doc_ids)/len(doc_ids)
        self.class_mean_weights = mean_weights

    def classify(self, weights):
        res = {}
        for doc_class, mean_weights in self.class_mean_weights.items():
            res[doc_class] = self.distance_func(weights, mean_weights)
        return sorted(res.items())
