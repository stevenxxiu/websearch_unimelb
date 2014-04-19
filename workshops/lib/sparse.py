
class RowDictMatrix:
    '''
    a list of rows stored as dicts has much faster indexing than using indptr's in csr sparse matrices
    '''

    @staticmethod
    def from_csr(X):
        # using a list of rows stored as dicts is much faster than using indptr's
        res = []
        for row in X:
            res.append(dict(zip(row.indices, row.data)))
        return res

    @staticmethod
    def vect_dot(d1, d2):
        res = 0
        for key in d1:
            if key in d2:
                res += d1[key] * d2[key]
        return res
