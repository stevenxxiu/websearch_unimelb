
import numpy as np
import scipy.linalg as la

def trim_small(X):
    X[np.absolute(X) < 0.000001] = 0.0

def main():
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
        S_d = np.zeros((5, 6))
        S_d[:d, :d] = np.diag(s[:d])
        X_d = np.dot(np.dot(U, S_d), V_T)
        trim_small(X_d)
        print(X_d)
        print(np.sum((np.array(X_d)-np.array(X))**2))

if __name__=='__main__':
    main()
