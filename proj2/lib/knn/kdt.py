
import numpy as np
from collections import namedtuple

TreeNode = namedtuple('Node', ('pivot', 'left', 'right'))

class KDTree:
    def __init__(self, distance):
        self.distance = distance
        self.X = None
        self.root = None
        self.n_traversed = 0

    def fit(self, X):
        self.X = X
        self.root = self._build_tree(list(range(X.shape[0])), 0)

    def _build_tree(self, points, depth):
        if not points:
            return None
        # select axis based on depth so that axis cycles through all valid values
        axis = depth % self.X.shape[1]
        # sort points based on the current axis
        points.sort(key=lambda i: self.X[i,axis])
        # choose the median as the pivot
        i = len(points)//2
        # Create node and construct subtrees
        return TreeNode(
            pivot = points[i],
            left = self._build_tree(points[:i], depth + 1),
            right_child = self._build_tree(points[i + 1:], depth + 1)
        )

    def search(self, q, k):
        # max heap
        nearest = [(-np.inf, None)] * k
        self._search(nearest, self.root, q)
        nearest = list(nearest)
        for i, (d, n) in enumerate(nearest):
            nearest[i] = (-d, n)
        return sorted(nearest)

    def _search(self, nearest, node, q):
        pass
