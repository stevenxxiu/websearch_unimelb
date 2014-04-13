
import numpy as np
from scipy.sparse import diags

def get_tf(X):
    X = X.copy()
    X.data = np.log(1 + np.array(X.data))
    return X

def get_dfs(X):
    return (X != 0).sum(0)

def get_idfs(X):
    num_docs = X.shape[0]
    return np.log(num_docs) - np.log(get_dfs(X))

def get_tf_idf(X):
    return get_tf(X)*diags(get_idfs(X).A1, 0)
