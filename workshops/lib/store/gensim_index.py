
from gensim import corpora, models

def lyrl_to_docs(coll_fname):
    """Convert a LYRL collection into the GenSim texts representation.
    
    The representation is very simple: a list of documents, where
    the documents are lists of terms.  We return (docids, docs), 
    where docids gives the ids of the documents."""
    curr_doc = None
    docs = []
    docids = []
    for line in open(coll_fname):
        line = line.strip()
        if line.startswith(".I"):
            (dot, docid) = line.split()
            curr_doc = []
            docids.append(docid)
        elif line.startswith(".W"):
            pass
        elif line == '':
            if curr_doc is not None:
                docs.append(curr_doc)
            curr_doc = None
        else:
            terms = line.split()
            curr_doc.extend(terms)
    if curr_doc is not None:
        docs.append(curr_doc)
    return docids, docs

def save_docids(docids, fname):
    """Save docids to file."""
    fp = open(fname, 'w')
    docnum = 0
    for docid in docids:
        fp.write("%s %d\n" % (docid, docnum))
        docnum += 1
    fp.close()

def get_docinfo_fname(tag):
    return "%s.docinfo.db" % tag

def get_dict_fname(tag):
    return "%s.dict.db" % tag

def get_corpus_fname(tag):
    return "%s.corp.db" % tag

def get_tfidf_fname(tag):
    return "%s.corp.tfidf.db" % tag

def make_index(coll_fname, index_tag):
    """Create a GenSim index of an LYRL collection.

    The index is contained in files whose names begin with
    index_tag.  index_tag may contain directories components,
    but the specified directories must already exist."""

    (docids, docs) = lyrl_to_docs(coll_fname)

    docinfo_fname = get_docinfo_fname(index_tag)
    dict_fname = get_dict_fname(index_tag)
    corpus_fname = get_corpus_fname(index_tag)
    tfidf_fname = get_tfidf_fname(index_tag)

    save_docids(docids, docinfo_fname)

    dict_ = corpora.Dictionary(docs)
    dict_.save(dict_fname)

    corpus = [ dict_.doc2bow(doc) for doc in docs ]
    corpora.MmCorpus.serialize(corpus_fname, corpus)
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    corpus_tfidf.save(tfidf_fname)
