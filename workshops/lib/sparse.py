
class RowDictMatrix:
    '''
    a list of rows stored as dicts has much faster indexing than using indptr's in csr sparse matrices
    '''

    @staticmethod
    def from_csr(X, dtype=None):
        '''
        args:
            dtype: type to convert to (python floats are faster than numpy floats if numpy is not used for operations)
        '''
        # using a list of rows stored as dicts is much faster than using indptr's
        res = []
        for row in X:
            if dtype is None:
                res.append(dict(zip(row.indices, row.data)))
            else:
                res.append(dict((i, dtype(data)) for i, data in zip(row.indices, row.data)))
        return res

    @staticmethod
    def vect_dot(d1, d2):
        res = 0
        if len(d1) > len(d2):
            d1, d2 = d2, d1
        for key in d1:
            if key in d2:
                res += d1[key] * d2[key]
        return res
