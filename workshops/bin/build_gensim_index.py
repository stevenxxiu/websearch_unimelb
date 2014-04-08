
from workshops.lib.gensim_index import make_index

if __name__ == '__main__':

    import sys

    if len(sys.argv) != 3:
        sys.stderr.write("USAGE: %s <lyrl-fname> <index-tag>\n" % (sys.argv[0]))
        sys.exit(1)

    lyrl_fname = sys.argv[1]
    index_tag = sys.argv[2]
    make_index(lyrl_fname, index_tag)
