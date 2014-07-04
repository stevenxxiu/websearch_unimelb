
import numpy as np
import bisect
from collections import namedtuple
from blist import sortedlist
from sklearn.decomposition import TruncatedSVD
from proj2.lib.linalg.dist import dist_sq_lt

TreeNode = namedtuple('TreeNode', ('points', 'p', 'gmins', 'gmaxes', 'children'))

class PrincipalAxisTree:
    def __init__(self, nc):
        '''
        Construct a principal axis tree for a list of row vectors.
        '''
        self.nc = nc
        self.X = None
        self.root = None
        self.pca = TruncatedSVD(1)

    def fit(self, X):
        self.X = X
        self.root = self._build_tree(np.array(range(X.shape[0])))

    def _build_tree(self, points):
        nc = self.nc
        ny = points.size
        pca = self.pca
        Y = self.X[points]
        if ny <= nc:
            # construct leaf node
            return TreeNode(points, None, None, None, ())
        # calculate the largest principal axis
        pca.fit(Y)
        p = pca.components_[0]
        # project vectors in Y onto the principal axis (unit vector)
        g = Y*p
        # divide vectors in G into regions with similar numbers of points
        i_sorted = np.argsort(g)
        i_parts = []
        offset = 0
        for i in range(nc-ny%nc):
            next_offset = offset + ny//nc
            i_parts.append(i_sorted[offset:next_offset])
            offset = next_offset
        for i in range(ny%nc):
            next_offset = offset + ny//nc + 1
            i_parts.append(i_sorted[offset:next_offset])
            offset = next_offset
        # calculate gmins & gmaxes, these two values form the bounds of the hyperplanes
        # each partition of points is in
        gmins = []
        gmaxes = []
        for i_part in i_parts:
            gmins.append(np.min(g[i_part]))
            gmaxes.append(np.max(g[i_part]))
        # construct children
        children = []
        for i_part in i_parts:
            children.append(self._build_tree(points[i_part]))
        return TreeNode(points, p, gmins, gmaxes, children)

    def search(self, q, k):
        nearest = sortedlist([(0, None)] * k)
        return self._search(nearest, self.root, q, q, 0)

    def _search(self, nearest, node, q, b, d_lb_sq):
        '''
        args:
            b: boundary point of the current convex hull being searched
        '''
        d_min_sq = nearest[0]
        X = self.X
        # check if node is a leaf node
        if not node.children:
            # partial distance search
            for p in node.points:
                if dist_sq_lt(q, X[p], d_min_sq):
                    d_min_sq = np.sum(np.power(q - X[p], 2))
                    nearest.add((d_min_sq, p))
                    nearest.pop(0)
        # project the boundary point onto the principal axis
        sigma = np.dot(b, node.p)
        # initialize stopping criteria vaiables
        # at least one is initialized to true, as there are at least 2 child nodes
        lower_done = False
        upper_done = False
        # find the closest group of points using sigma (projecting q instead of b may be more accurate here)
        nc = len(node.children)
        # perform a binary search
        # the boundary conditions don't matter here, as we will search both above and below until the
        # bounds are reached
        i = bisect.bisect_left(sigma, node.gmaxes)
        il = i - 1
        iu = i + 1
        if i == 0:
            lower_done = True
        elif i == nc-1:
            upper_done = True
        # search the region b is in
        self._search(nearest, node.children[i], q, b, d_lb_sq)
        # initialize distances
        if not lower_done:
            while il>=0:
                dl = sigma - node.gmaxes[il]
                cur_d_lb_sq = d_lb_sq + dl**2
                if nearest[-1][0] <= cur_d_lb_sq:
                    # lower bound is exceeded for the child
                    break
                if not node.children[il].children:
                    # calculate the boundary point
                    bl = b - dl*node.p
                else:
                    bl = 0
                self._search(nearest, node.children[il], q, bl, cur_d_lb_sq)
                il -= 1
        if not upper_done:
            while iu<nc:
                du = node.gmaxes[iu] - sigma
                cur_d_lb_sq = d_lb_sq + du**2
                if nearest[-1][0] <= cur_d_lb_sq:
                    # lower bound is exceeded for the child
                    break
                if not node.children[iu].children:
                    # calculate the boundary point
                    bu = du*node.p - b
                else:
                    bu = 0
                self._search(nearest, node.children[il], q, bu, cur_d_lb_sq)
                iu += 1

