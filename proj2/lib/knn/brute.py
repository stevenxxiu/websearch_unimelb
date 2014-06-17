
import numpy as np
from workshops.lib.weights import l2_sparse

class KNeighborsBrute:
    def __init__(self):
        self.X = None
        self.X_l2_sq = None

    def fit(self, X):
        self.X = X
        self.X_l2_sq = np.power(l2_sparse(X), 2)

    def kneighbors(self, y, k=None):
        dists = np.asarray(np.sqrt(self.X_l2_sq + np.power(l2_sparse(y), 2).T - 2*self.X*y.T).T)[0]
        if k is None:
            k = self.X.shape[0]
        indexes = np.argsort(dists)
        return list(zip(dists[indexes[:k]], indexes[:k]))
