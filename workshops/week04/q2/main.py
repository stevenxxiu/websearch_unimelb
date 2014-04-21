
import numpy as np
import scipy.linalg as la

def trim_small(X):
    # noinspection PyUnresolvedReferences
    X[np.absolute(X) < 0.000001] = 0.0

def main():
    # noinspection PyCallingNonCallable
    X = np.matrix([
        [1, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0],
        [1, 0, 0, 1, 1, 0],
        [0, 0, 0, 1, 0, 1],
    ])
    (U, s, V_T) = la.svd(X)
    trim_small(U)
    trim_small(V_T)
    print('U, s, V_T:')
    print(U)
    print(s)
    print(V_T)
    S_ = np.zeros((5, 6))
    S_[:5, :5] = np.diag(s)
    X_ = np.dot(np.dot(U, S_), V_T)
    trim_small(X_)
    print(X_)

if __name__=='__main__':
    main()
