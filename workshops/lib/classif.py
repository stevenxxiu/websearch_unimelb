
import heapq
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


class KNN:
    def __init__(self, distance_func):
        self.distance_func = distance_func
        self.train_docs = []
        self.docs_db = None

    def train(self, train_docs, docs_db):
        self.train_docs = train_docs
        self.docs_db = docs_db

    def classify(self, weights, k):
        closest = []
        # find the nearest k training documents
        for doc_id, doc_classes in self.train_docs:
            dist = self.distance_func(weights, self.docs_db.find_one({'doc_id': doc_id})['weights'])
            heapq.heappush(closest, (-dist, doc_id))
            if len(closest)>k:
                heapq.heappop(closest)
        res = {}
        train_docs_dict = dict(self.train_docs)
        for dist, doc_id in closest:
            for doc_class in train_docs_dict[doc_id]:
                res.setdefault(doc_class, 0)
                res[doc_class] += 1
        num_classes = sum(res.values())
        for doc_class in res:
            res[doc_class]/=num_classes
        return sorted(res.items(), key=lambda doc_score: (doc_score[1], doc_score[0]), reverse=True)

