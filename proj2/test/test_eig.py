
import unittest
import numpy as np
from proj2.lib.linalg import eig

class TestEigen(unittest.TestCase):
    # noinspection PyCallingNonCallable
    def test_first_eigenvector(self):
        self.assertTrue(np.allclose(eig.first_eigenvector(np.matrix([[1, 2], [3, 4]])), [[0.41597356], [0.90937671]]))

    # noinspection PyCallingNonCallable
    def test_first_sparse_pca(self):
        X = np.matrix([[ 1,  1], [2,  4], [3, 9], [ 4,  16], [ 5,  25], [ 6,  36]])
        self.assertTrue(np.allclose(eig.first_sparse_pca(X), [0.13573869, 0.99074467]))
