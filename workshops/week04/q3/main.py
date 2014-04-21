
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
    # s is sorted in decreasing order
    for d in range(5, 0, -1):
        S_d = np.zeros((d, d))
        S_d[:d, :d] = np.diag(s[:d])
        U_d = U[:,:d]
        V_d_T = V_T[:d,:]
        X_d = np.dot(np.dot(U_d, S_d), V_d_T)
        trim_small(X_d)
        print(X_d)
        print(np.sum((np.array(X_d)-np.array(X))**2))

if __name__=='__main__':
    main()
