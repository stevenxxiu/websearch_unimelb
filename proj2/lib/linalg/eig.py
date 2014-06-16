
import numpy as np

def power_iter(X, max_iter=100, tol=1.0e-8):
    '''
    Find the eigenvector corresponding the the largest eigenvalue using power iteration.
    Doesn't converge if the largest eigenvalue has multiplicity > 1, but still can be used as an approximation tool.
    '''
    b = np.random.random_sample((X.shape[0], 1))
    for i in range(max_iter):
        b_prev = b
        b = X * b
        # normalize b
        b *= 1/np.sqrt(np.sum(np.power(b, 2)))
        # l1 norm
        err = np.sum(b - b_prev)
        if abs(err) < tol:
            break
    else:
        raise ValueError('power iteration failed to converge in {} iterations'.format(max_iter))
    return b
