
from numba import double, boolean
from numba.decorators import jit

@jit(boolean(double[:], double[:], double))
def dist_sq_lt(u, v, b):
    '''
    Does a partial distance search to see if dist(u, v)**2<b, for l2 distances.
    '''
    d = 0
    for x in range(u.size):
        d += (u[x] - v[x])**2
        if d>=b:
            return False
    return True
