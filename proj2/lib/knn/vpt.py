
import heapq
import random
import statistics
import numpy as np

class TreeNode:
    def __init__(self, p, left, right, lower_bnd, upper_bnd):
        self.p = p
        self.left = left
        self.right = right
        self.lower_bnd = lower_bnd
        self.upper_bnd = upper_bnd

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
        self.root = self._build_tree(list(range(X.shape[0])))

    def _build_tree(self, points):
        if len(points) == 0:
            return None
        elif len(points) == 1:
            node = TreeNode(points[0], None, None, None, None)
            return node
        node = TreeNode(None, None, None, None, None)
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
        if left_dists:
            node.left.lower_bnd = min(left_dists)
            node.left.upper_bnd = max(left_dists)
        if right_dists:
            node.right.lower_bnd = min(right_dists)
            node.right.upper_bnd = max(right_dists)
        return node

    @staticmethod
    def _select_vp(items):
        # pick a random item
        return random.randrange(len(items))

    def search(self, q, k):
        self.n_traversed = 0
        # max heap
        nearest = [(-np.inf, None)] * k
        self._search(nearest, self.root, q)
        nearest = list(nearest)
        for i, (d, n) in enumerate(nearest):
            nearest[i] = (-d, n)
        return sorted(nearest)

    def _search(self, nearest, node, q):
        if not node:
            return
        tau = -nearest[0][0]
        x = self.distance(q, self.X[node.p])
        self.n_traversed += 1
        if x < tau:
            tau = x
            heapq.heapreplace(nearest, (-x, node.p))
        if node.left and node.right:
            middle = (node.left.upper_bnd + node.right.lower_bnd)/2
            if x < middle:
                if node.left.lower_bnd - tau < x < node.left.upper_bnd + tau:
                    self._search(nearest, node.left, q)
                if node.right.lower_bnd - tau < x < node.right.upper_bnd + tau:
                    self._search(nearest, node.right, q)
            else:
                if node.right.lower_bnd - tau < x < node.right.upper_bnd + tau:
                    self._search(nearest, node.right, q)
                if node.left.lower_bnd - tau < x < node.left.upper_bnd + tau:
                    self._search(nearest, node.left, q)
        elif node.left and not node.right:
            if node.left.lower_bnd - tau < x < node.left.upper_bnd + tau:
                self._search(nearest, node.left, q)
        elif node.right and not node.left:
            if node.right.lower_bnd - tau < x < node.right.upper_bnd + tau:
                self._search(nearest, node.right, q)
