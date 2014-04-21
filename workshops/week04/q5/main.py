
import os
import gensim
from gensim import corpora
from workshops.lib.store import gensim_index

def main():
    data_path = '../../../../data/'
    gensim_index_path = '../../../../data/gensim/'
    gensim_index_tag = 'idx'
    term_dict = corpora.Dictionary.load(os.path.join(gensim_index_path, gensim_index.get_dict_fname(gensim_index_tag)))
    corpus = corpora.MmCorpus(os.path.join(gensim_index_path, gensim_index.get_corpus_fname(gensim_index_tag)))
    lsi = gensim.models.lsimodel.LsiModel(corpus=corpus, id2word=term_dict, num_topics=20)
    query = 'offic'
    query_bow = term_dict.doc2bow(query.lower().split())
    # convert the query to LSI space
    query_lsi = lsi[query_bow]
    # transform corpus to LSI space and index it
    index = gensim.similarities.MatrixSimilarity(lsi[corpus])
    # perform a similarity query against the corpus
    sims = index[query_lsi]
    # print (document_number, document_similarity) 2-tuples
    query_res = sorted(list(enumerate(sims)), key=lambda x: x[1], reverse=True)
    doc_ids, docs = gensim_index.lyrl_to_docs(os.path.join(data_path, 'lyrl_tokens_30k.dat'))
    for doc_matrix_id, sim in query_res[:10]:
        print(sim, doc_ids[doc_matrix_id], docs[doc_matrix_id])

if __name__=='__main__':
    main()
