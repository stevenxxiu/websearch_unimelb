
import random
import heapq
import statistics
import numpy as np
from operator import itemgetter
from collections import namedtuple

TreeNode = namedtuple('TreeNode', ('p', 'left', 'right', 'lower_bnd', 'upper_bnd'))

class VPTree:
    '''
    A vp tree with subspace bounds.
    '''
    def __init__(self, distance):
        self.distance = distance
        self.X = None
        self.root = None
        self.n_traversed = 0

    def fit(self, X):
        self.X = X
        self.root = self._build_tree(np.array(range(X.shape[0])))

    def _build_tree(self, points):
        if not points:
            return None
        node = TreeNode()
        p_i = self._select_vp(points)
        node.p = points[p_i]
        points.pop(p_i)
        # compute distances
        dists = []
        for point in points:
            dists.append(self.distance(self.X[node.p], self.X[point]))
        # compute the median distance to the current vantage point
        mu = statistics.median(dists)
        left_points = []
        right_points = []
        left_dists = []
        right_dists = []
        for i, dist in enumerate(dists):
            if dist < mu:
                left_points.append(points[i])
                left_dists.append(dist)
            else:
                right_points.append(points[i])
                right_dists.append(dist)
        # create children
        node.left = self._build_tree(left_points)
        node.right = self._build_tree(right_points)
        # calculate bounds of each child node with regards to p
        node.left.lower_bnd = min(left_dists)
        node.left.upper_bnd = max(left_dists)
        node.left.lower_bnd = min(left_dists)
        node.left.upper_bnd = max(left_dists)
        return node

    def _select_vp(self, items):
        # pick a random item
        return random.choice(len(items))

