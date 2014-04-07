import shelve

from workshops.lib import coll


def mkind(coll, filename):
    """Create a doc:docvec shelf index of a collection in a filename."""

    index = shelve.open(filename)
    for doc in coll:
        index[doc.get_docid()] = doc.get_term_freq_dict()
    index.close()

if __name__ == '__main__':

    import sys

    if len(sys.argv) != 3:
        sys.stderr.write("USAGE: %s <coll-file> <db-file>\n" % sys.argv[0])
        sys.exit()
    coll_ = coll.parse_lyrl_coll(sys.argv[1])
    mkind(coll_, sys.argv[2])
