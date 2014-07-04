
import numpy as np
from scipy import sparse
from scipy.misc import logsumexp

# noinspection PyUnresolvedReferences
def mode(a, axis=0, dtype=None):
    scores = np.unique(np.ravel(a))
    testshape = list(a.shape)
    testshape[axis] = 1
    oldmostfreq = np.zeros(testshape, dtype=dtype)
    oldcounts = np.zeros(testshape, dtype=dtype)
    mostfrequent = np.array([])
    for score in scores:
        template = (a == score)
        counts = np.expand_dims(np.sum(template, axis),axis)
        mostfrequent = np.where(counts > oldcounts, score, oldmostfreq)
        oldcounts = np.maximum(counts, oldcounts)
        oldmostfreq = mostfrequent
    return mostfrequent, oldcounts


# noinspection PyUnresolvedReferences
def get_train_test(n, ntrain, ntest, reproducible=True):
    '''
    Assumes all documents are labelled.

    returns:
        (train_indexes, test_indexes)
    '''
    if reproducible:
        np.random.seed(1)
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

    # noinspection PyNoneFunctionAssignment
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
        dists = self.distance_func(X, self.X)
        if sparse.isspmatrix(dists):
            dists = dists.todense()
        closest_docs = dists.argsort(axis=1)[:,:k]
        return mode(self.y[closest_docs], axis=1, dtype=int)[0].T[0]


class MultinomialNB:
    def __init__(self):
        self.classes = None
        self.class_weights = None
        self.term_weights = None

    # noinspection PyNoneFunctionAssignment,PyUnresolvedReferences
    def fit(self, X, y):
        # calculate the class-dependent term term_weights
        n_samples, n_features = X.shape
        classes = np.unique(y)
        self.classes = classes
        n_classes = classes.size
        self.term_weights = np.empty((n_classes, n_features), dtype=np.float64)
        for class_ in classes:
            term_freqs = X[y==class_].sum(axis=0)
            # use laplace smoothing, the matrix includes non-zero weights
            self.term_weights[class_] = np.log(term_freqs + 1) - np.log(term_freqs.sum() + n_features)
        # calculate weights of class-priors
        self.class_weights = np.empty((n_classes, 1), dtype=np.float64)
        for class_ in classes:
            self.class_weights[class_] = np.log(X[y==class_].shape[0]) - np.log(n_samples)

    def score(self, X):
        return self.class_weights.T + X * self.term_weights.T

    def predict(self, X):
        return self.score(X).argmax(axis=1)

    def predict_proba(self, X):
        score = self.score(X)
        return np.exp(score.T - logsumexp(score, axis=1)).T
