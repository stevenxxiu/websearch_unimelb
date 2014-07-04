
import heapq
import numpy as np
from collections import namedtuple
from proj2.lib.linalg.eig import first_sparse_pca

TreeNode = namedtuple('TreeNode', ('points', 'p', 'gmins', 'gmaxes', 'children'))

class PrincipalAxisTree:
    def __init__(self, nc):
        '''
        Construct a principal axis tree for a list of row vectors.
        '''
        self.nc = nc
        self.X = None
        self.root = None
        self.n_traversed = 0

    def fit(self, X):
        self.X = X
        self.root = self._build_tree(np.array(range(X.shape[0])))

    def _build_tree(self, points):
        nc = self.nc
        ny = points.size
        Y = self.X[points]
        if ny <= nc:
            # construct leaf node
            return TreeNode(points, None, None, None, ())
        # calculate the largest principal axis
        p = first_sparse_pca(Y, 1000)
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
            gmins.append(g[i_part[0]])
            gmaxes.append(g[i_part[-1]])
        # construct children
        children = []
        for i_part in i_parts:
            children.append(self._build_tree(points[i_part]))
        # points only needs to be stored for leaf nodes
        return TreeNode(None, p, gmins, gmaxes, children)

    def search(self, q, k):
        self.n_traversed = 0
        # max heap
        nearest = [(-np.inf, None)] * k
        self._search(nearest, self.root, q, q, 0)
        nearest = list(nearest)
        for i, (d, n) in enumerate(nearest):
            nearest[i] = (np.sqrt(-d), n)
        return sorted(nearest)

    # noinspection PyTypeChecker,PyUnresolvedReferences
    def _search(self, nearest, node, q, b, d_lb_sq):
        '''
        args:
            b: boundary point of the current convex hull being searched
        '''
        X = self.X
        # check if node is a leaf node
        if not node.children:
            d_k_sq = -nearest[0][0]
            for p in node.points:
                d_sq = np.sum(np.power((q - X[p]).data, 2))
                if d_sq < d_k_sq:
                    heapq.heapreplace(nearest, (-d_sq, p))
                    d_k_sq = -nearest[0][0]
            self.n_traversed += node.points.size
            return
        # project the boundary point onto the principal axis
        sigma = (b*node.p)[0]
        # initialize stopping criteria vaiables
        # at least one is initialized to true, as there are at least 2 child nodes
        lower_done = False
        upper_done = False
        nc = len(node.children)
        # perform a binary search using sigma
        # the boundary conditions don't matter here, as we will search both above and below until the
        # bounds are reached
        i = np.searchsorted(node.gmaxes, sigma)
        il = i - 1
        iu = i + 1
        if il < 0:
            lower_done = True
        if iu > nc-1:
            upper_done = True
        # search the region b is in
        if 0 <= i <= nc-1:
            self._search(nearest, node.children[i], q, b, d_lb_sq)
        # initialize distances
        dl = du = 0
        bl = bu = 0
        if not lower_done:
            dl = sigma - node.gmaxes[il]
        if not upper_done:
            du = node.gmins[iu] - sigma
        while not upper_done or not lower_done:
            if (upper_done or dl<du) and not lower_done:
                cur_d_lb_sq = d_lb_sq + dl**2
                if -nearest[0][0] <= cur_d_lb_sq:
                    # lower bound is exceeded for the child
                    lower_done = True
                    continue
                if not node.children[il].children:
                    # calculate the boundary point
                    bl = b - dl*node.p
                self._search(nearest, node.children[il], q, bl, cur_d_lb_sq)
                il -= 1
                if il < 0:
                    lower_done = True
                    continue
                dl = sigma - node.gmaxes[il]
            else:
                cur_d_lb_sq = d_lb_sq + du**2
                if -nearest[0][0] <= cur_d_lb_sq:
                    # lower bound is exceeded for the child
                    upper_done = True
                    continue
                if not node.children[iu].children:
                    # calculate the boundary point
                    bu = b + du*node.p
                self._search(nearest, node.children[iu], q, bu, cur_d_lb_sq)
                iu += 1
                if iu > nc-1:
                    upper_done = True
                    continue
                du = node.gmins[iu] - sigma

