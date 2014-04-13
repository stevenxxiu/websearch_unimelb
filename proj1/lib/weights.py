
import numpy as np
from scipy.sparse import diags

def l2_norm_sparse(X):
    '''
    l2 norm for all row vectors (np.linalg.norm doesn't work).
    '''
    norms = X.copy()
    norms.data **= 2
    norms = np.sqrt(norms.sum(axis=1))
    return diags(1/norms.A1, 0) * X


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
