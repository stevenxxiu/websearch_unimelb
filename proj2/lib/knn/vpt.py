
import random
import heapq
import statistics
import numpy as np
from collections import namedtuple

TreeNode = namedtuple('TreeNode', ('p', 'left', 'right', 'bnds'))
Item = namedtuple('Item', ('p', 'hist'))

class VPTree:
    '''
    A vps tree.
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
        items = list(Item(point, list()) for point in points)
        return self._recurse_tree(items)

    def _recurse_tree(self, items):
        if not items:
            return None
        node = TreeNode()
        p_i = self._select_vp(items)
        node.p = items[p_i]
        items.pop(p_i)
        # append all distances to the current vantage point to hist
        for item in items:
            item.hist.append(self.distance(node.p, item.p))
        # compute the median distance to the current vantage point
        mu = statistics.median(item.hist[-1] for item in items)
        left_items = []
        right_items = []
        for item in items:
            if item.hist[-1] < mu:
                left_items.append(item)
            else:
                right_items.append(item)
        node.left = self._recurse_tree(left_items)
        node.right = self._recurse_tree(right_items)
        # calculate bounds
        hist_len = len(node.p.hist)
        if node.left is not None and node.right is not None:
            node.bnds = []
            for lb, rb, pd in zip(node.left.bnds[:hist_len], node.right.bnds[:hist_len], node.p.hist):
                node.bnds.append((min(lb[0], rb[0], pd), max(lb[1], rb[1], pd)))
        elif node.left is not None:
            node.bnds = []
            for lb, pd in zip(node.left.bnds[:hist_len], node.p.hist):
                node.bnds.append((min(lb[0], pd), max(lb[1], pd)))
        elif node.right is not None:
            node.bnds = []
            for rb, pd in zip(node.right.bnds[:hist_len], node.p.hist):
                node.bnds.append((min(rb[0], pd), max(rb[1], pd)))
        else:
            node.bnds = node.p.hist
        return node

    def _select_vp(self, items):
        # pick a random item
        return random.choice(len(items))

