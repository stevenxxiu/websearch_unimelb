
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
