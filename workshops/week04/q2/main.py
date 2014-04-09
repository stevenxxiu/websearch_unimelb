
import numpy as np
import scipy.linalg as la

def main():
    X = np.matrix([
        [1, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0],
        [1, 0, 0, 1, 1, 0],
        [0, 0, 0, 1, 0, 1],
    ])
    (U, s, V_T) = la.svd(X)
    print(X.shape, U.shape, V_T.shape)
    U[np.absolute(U) < 0.000001] = 0.0
    V_T[np.absolute(V_T) < 0.000001] = 0.0
    print('U, s, V_T:')
    print(U)
    print(s)
    print(V_T)
    S_ = np.zeros((5, 6))
    S_[:5, :5] = np.diag(s)
    X_ = np.dot(np.dot(U, S_), V_T)
    X_[np.absolute(X_) < 0.000001] = 0.0
    print(X_)

if __name__=='__main__':
    main()
