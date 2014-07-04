
import heapq
import numpy as np
from collections import namedtuple

TreeNode = namedtuple('Node', ('p', 'left', 'right', 'left_lower_bnd', 'right_lower_bnd'))

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
        i_mu = len(points)//2
        mu = self.X[points[i_mu],axis]
        left_lower_bnd = mu - self.X[points[i_mu-1],axis] if i_mu-1>=0 else None
        right_lower_bnd = self.X[points[i_mu+1],axis] - mu if i_mu+1<len(points) else None
        # create node and construct subtrees
        return TreeNode(
            p = points[i_mu],
            left = self._build_tree(points[:i_mu], depth+1),
            right_child = self._build_tree(points[i_mu+1:], depth+1),
            left_lower_bnd = left_lower_bnd,
            right_lower_bnd = right_lower_bnd
        )

    def search(self, q, k):
        # max heap
        nearest = [(-np.inf, None)] * k
        self._search(nearest, self.root, q, 0)
        nearest = list(nearest)
        for i, (d, n) in enumerate(nearest):
            nearest[i] = (-d, n)
        return sorted(nearest)

    def _search(self, nearest, node, q, depth):
        if not node:
            return
        axis = depth % self.X.shape[1]
        # compare with pivot
        d = -nearest[0][0]
        x = self.distance(q, self.X[node.p])
        self.n_traversed += 1
        if x < d:
            d = x
            heapq.heapreplace(nearest, (-d, node.p))
        # check if left/right nodes need to be visited, visit the one with lower minimum axis distance first
        mu = self.X[node.p,axis]
        left_dist = q[axis] - mu + node.left_lower_bnd
        right_dist = mu - q[axis] + node.left_lower_bnd
        if node.left and node.right:
            if left_dist < right_dist:
                if left_dist <= d:
                    self._search(nearest, node.left, q, depth+1)
                if right_dist <= d:
                    self._search(nearest, node.right, q, depth+1)
            else:
                if right_dist <= d:
                    self._search(nearest, node.right, q, depth+1)
                if left_dist <= d:
                    self._search(nearest, node.left, q, depth+1)
        elif node.left and not node.right:
            if left_dist <= d:
                self._search(nearest, node.left, q, depth+1)
        elif node.right and not node.left:
            if right_dist <= d:
                self._search(nearest, node.right, q, depth+1)
