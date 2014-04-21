
import pickle
from workshops.lib.weights import l2_norm_sparse
from workshops.lib.features import get_tf_idf

def doc_similarity(doc_id_1, doc_id_2, tf_idfs, dataset):
    return (tf_idfs[dataset.doc_indexes[doc_id_1]] * tf_idfs[dataset.doc_indexes[doc_id_2]].T).data[0]

def main():
    with open('../../../../data/pickle/lyrl.db', 'rb') as sr:
        # noinspection PyArgumentList
        dataset = pickle.load(sr)
        tf_idfs = l2_norm_sparse(get_tf_idf(dataset.freq_matrix))
        print(doc_similarity('26152', '26159', tf_idfs, dataset))
        print(doc_similarity('26152', '26413', tf_idfs, dataset))

if __name__ == '__main__':
    main()
