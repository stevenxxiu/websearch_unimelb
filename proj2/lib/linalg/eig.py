
import numpy as np

# noinspection PyTypeChecker,PyUnresolvedReferences
def first_eigenvector(X, max_iter=100, tol=1.0e-8):
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

# noinspection PyTypeChecker,PyUnresolvedReferences
def first_sparse_pca(X, max_iter=100, tol=1.0e-8):
    '''
    Sklearn's implementation does not normalize to mean 0 first.
    '''
    b = np.random.random_sample((X.shape[1], 1))
    for i in range(max_iter):
        b_prev = b
        # calculate b = (X - X.mean(axis=0)).T * (X - X.mean(axis=0)) * b while preserving sparsity
        b = X.T*(X*b) - X.sum(axis=0).T*(X.mean(axis=0)*b)
        # normalize b
        b *= 1/np.sqrt(np.sum(np.power(b, 2)))
        # l1 norm
        err = np.sum(b - b_prev)
        if abs(err) < tol:
            break
    else:
        raise ValueError('power iteration failed to converge in {} iterations'.format(max_iter))
    return b
