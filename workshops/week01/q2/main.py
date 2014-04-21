
import numpy as np
import pickle
from workshops.lib.features import get_dfs

def main():
    with open('../../../../data/pickle/lyrl.db', 'rb') as sr:
        # noinspection PyArgumentList
        dataset = pickle.load(sr)
        dfs = np.array(get_dfs(dataset.freq_matrix))[0]
        print('{:<50}{:}'.format('TERM', 'DOC_FREQ'))
        # noinspection PyTypeChecker
        for i in np.argsort(-dfs):
            print('{:<50}{:}'.format(dataset.terms[i], dfs[i]))

if __name__ == '__main__':
    main()
