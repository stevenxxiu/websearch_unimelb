
import math
from collections import Counter

class WeightDict(Counter):
    def __mul__(self, other):
        res = WeightDict()
        for key, value in self.items():
            res[key] = value*other
        return res

    def __rmul__(self, other):
        res = WeightDict()
        for key, value in self.items():
            res[key] = value*other
        return res

    def __truediv__(self, other):
        return self*(1/other)

def l2_dist(weights):
    return math.sqrt(sum(v**2 for v in weights.values()))

def l2_norm(weights):
    res = {}
    norm = l2_dist(weights)
    for key, value in weights.items():
        res[key] = value/norm
    return res

class PivotedLengthNorm:
    def __init__(self, distance_func, docs_weights):
        self.distance_func = distance_func
        # find doc_length_average
        doc_length_total = 0
        i=None
        for i, weights in enumerate(docs_weights):
            doc_length_total += distance_func(weights)
        if i is not None:
            # don't use len() in case docs_weights is an iterator
            doc_length_total/=i+1
        self.doc_length_average = doc_length_total

    def norm(self, weights, slope):
        res = {}
        alpha = ((1-slope)*self.doc_length_average + slope*self.distance_func(weights))
        for key, value in weights.items():
            res[key] = value/alpha
        return res

def cosine_similarity(weight_dict_1, weight_dict_2):
    '''
    assumes that both weight_dict_1 and weight_dict_2 are normalized
    '''
    score = 0
    for term in weight_dict_1:
        if term in weight_dict_2:
            score += weight_dict_1[term]*weight_dict_2[term]
    return score
