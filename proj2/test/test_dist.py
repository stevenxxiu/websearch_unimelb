
import timeit
import unittest
import numpy as np
import textwrap
from proj2.lib.linalg import dist

class TestDist(unittest.TestCase):
    def bench_dist_sq_lt(self):
        print(timeit.timeit(stmt='dist.dist_sq_lt(u, v, 2.5)', setup=textwrap.dedent("""
            import numpy as np
            from proj2.lib.linalg import dist
            u = np.array([1., 1., 1.])
            v = np.array([2., 2., 2.])
        """), number=10000))

    def test_dist_sq_lt(self):
        self.assertTrue(dist.dist_sq_lt(np.array([1., 1., 1.]), np.array([2., 2., 2.]), 3.5))
