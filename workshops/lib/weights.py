
import numpy as np
from scipy.sparse import diags

def l2_norm_sparse(X):
    '''
    l2 norm for all row vectors (np.linalg.norm doesn't work).
    '''
    norms = X.copy()
    norms.data **= 2
    norms = np.sqrt(norms.sum(axis=1))
    # noinspection PyUnresolvedReferences
    return diags(1/norms.A1, 0) * X

def l2_sparse(X):
    norms = X.copy()
    norms.data **= 2
    return np.sqrt(norms.sum(axis=1))

def cdist(X, Y):
    '''
    Pairwise euclidean distance for all row vectors (scipy.spatial.distance.cdist doesn't support sparse matrices).
    The nth row in the output corresponds to the distances of the nth row of X to Y.
    '''
    # noinspection PyUnresolvedReferences
    return np.sqrt(np.power(l2_sparse(X), 2) + np.power(l2_sparse(Y), 2).T - 2*X*Y.T)
