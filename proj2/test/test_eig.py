
import unittest
import numpy as np
from proj2.lib.linalg import eig

class TestEigen(unittest.TestCase):
    def test_power_iter(self):
        self.assertTrue(np.allclose(eig.power_iter(np.matrix([[1, 2], [3, 4]])), [[ 0.41597356], [ 0.90937671]]))
