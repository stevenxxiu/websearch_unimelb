
import numpy as np
from collections import namedtuple
from proj2.lib.linalg.eig import power_iter

TreeNode = namedtuple('TreeNode', ('points', 'p', 'gmins', 'gmaxes', 'children'))

class PrincipalAxisTree:
    def __init__(self, X, nc):
        '''
        Construct a principal axis tree for a list of column vectors.
        '''
        self.X = X
        self.nc = nc
        self.root = self.build_tree(tuple(range(X.shape[1])))

    def build_tree(self, points):
        nc = self.nc
        ny = points.size[0]
        Y = self.X[points]
        if ny < nc:
            # construct terminal node
            return TreeNode(points, None, None, None, ())
        # convert Y to a matrix with mean 0
        Y -= np.mean(Y, axis=1)
        # calculate the largest principal axis
        p = power_iter(Y.T*Y)
        # project vectors in Y onto principal axis
        g = Y*p
        # divide vectors in G into regions with similar numbers of points
        points_sorted = points[np.argsort(g)]
        parts = []
        offset = 0
        for i in range(ny//nc):
            next_offset = offset + nc
            parts.append(points_sorted[offset:next_offset])
            offset = next_offset
        for i in range(ny%nc):
            next_offset = offset + nc + 1
            parts.append(points_sorted[offset:next_offset])
            offset = next_offset
        # calculate gmins & gmaxes
        gmins = []
        gmaxes = []
        for part in parts:
            gmins.append(np.min(g[part]))
            gmaxes.append(np.max(g[part]))
        # construct children
        children = []
        for part in parts:
            children.append(self.build_tree(part))
        return TreeNode(points, p, gmins, gmaxes, children)

    def search(self):
        pass
