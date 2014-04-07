
from workshops.lib.weights import WeightDict

class Rocchio:
    def __init__(self, distance_func):
        self.class_mean_weights = {}
        self.distance_func = distance_func

    def train(self, train_docs, docs_db):
        class_nums = {}
        total_weights = {}
        for doc_id, doc_classes in train_docs:
            for doc_class in doc_classes:
                total_weights.setdefault(doc_class, WeightDict())
                total_weights[doc_class] += WeightDict(docs_db.find_one({'doc_id': doc_id})['weights'])
                class_nums.setdefault(doc_class, 0)
                class_nums[doc_class] += 1
        mean_weights = {}
        for doc_class in class_nums.keys():
            mean_weights[doc_class] = total_weights[doc_class]/class_nums[doc_class]
        self.class_mean_weights = mean_weights

    def classify(self, weights):
        res = {}
        for doc_class, mean_weights in self.class_mean_weights.items():
            res[doc_class] = self.distance_func(weights, mean_weights)
        return sorted(res.items(), key=lambda doc_score: (doc_score[1], doc_score[0]))
