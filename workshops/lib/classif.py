
import numpy as np

def mode(a, axis=0, dtype=None):
    scores = np.unique(np.ravel(a))
    testshape = list(a.shape)
    testshape[axis] = 1
    oldmostfreq = np.zeros(testshape, dtype=dtype)
    oldcounts = np.zeros(testshape, dtype=dtype)
    for score in scores:
        template = (a == score)
        counts = np.expand_dims(np.sum(template, axis),axis)
        mostfrequent = np.where(counts > oldcounts, score, oldmostfreq)
        # noinspection PyUnresolvedReferences
        oldcounts = np.maximum(counts, oldcounts)
        oldmostfreq = mostfrequent
    # noinspection PyUnboundLocalVariable
    return mostfrequent, oldcounts


def get_train_test(n, ntrain, ntest, reproducible=True):
    '''
    Assumes all documents are labelled.

    returns:
        (train_indexes, test_indexes)
    '''
    if reproducible:
        # noinspection PyUnresolvedReferences
        np.random.seed(1)
    # noinspection PyUnresolvedReferences
    perm = np.random.permutation(n)
    return perm[:ntrain], perm[ntrain:ntrain+ntest]


class Rocchio:
    def __init__(self, distance_func):
        '''
        args:
            distance_func: returns the pairwise distances between two lists of vectors
        '''
        self.distance_func = distance_func
        self.centroids = None
        self.classes = None

    def fit(self, X, y):
        n_samples, n_features = X.shape
        classes = np.unique(y)
        self.classes = classes
        n_classes = classes.size
        self.centroids = np.empty((n_classes, n_features), dtype=np.float64)
        for class_ in classes:
            self.centroids[class_] = X[y==class_].mean(axis=0)

    def predict(self, X):
        return self.classes[self.distance_func(X, self.centroids).argmin(axis=1)]


class KNN:
    def __init__(self, distance_func):
        self.distance_func = distance_func
        self.X = None
        self.y = None

    def fit(self, X, y):
        self.X = X
        self.y = y

    def predict(self, X, k):
        # find the nearest k training documents
        closest_docs = self.distance_func(X, self.X).todense().argsort(axis=1)[:,:k]
        return mode(self.y[closest_docs], axis=1, dtype=int)[0].T[0]

