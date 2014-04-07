
import math
from collections import Counter

class WeightDict(Counter):
    def __mul__(self, other):
        res = WeightDict()
        for key, value in self.items():
            res[key] = value*other
        return res

    def __truediv__(self, other):
        return self*(1/other)

def normalize_weights(weights):
    res = {}
    # l2 norm
    norm = math.sqrt(sum(v**2 for v in weights.values()))
    for key, value in weights.items():
        res[key] = value/norm
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
