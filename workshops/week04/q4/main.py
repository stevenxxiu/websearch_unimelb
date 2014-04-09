
import os
import gensim
from gensim import corpora
from workshops.lib import gensim_index

def main():
    gensim_index_path = '../../../../data/gensim/'
    gensim_index_tag = 'idx'
    term_dict = corpora.Dictionary.load(os.path.join(gensim_index_path, gensim_index.get_dict_fname(gensim_index_tag)))
    corpus = corpora.MmCorpus(os.path.join(gensim_index_path, gensim_index.get_corpus_fname(gensim_index_tag)))
    lsi = gensim.models.lsimodel.LsiModel(corpus=corpus, id2word=term_dict, num_topics=20)
    print('\n'.join(lsi.print_topics(20, num_words=20)))

if __name__=='__main__':
    main()
