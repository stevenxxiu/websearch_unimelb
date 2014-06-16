
from collections import namedtuple

TreeNode = namedtuple('TreeNode', ('p', 'gmins', 'gmaxs', 'points'))

class PrincipalAxisTree:
    def __init__(self, X, nc):
        self.X = X
        self.nc = nc
        self.root = self.build_tree(tuple(range(X.shape[0])))

    def build_tree(self, points):
        pass

    def search(self):
        pass
