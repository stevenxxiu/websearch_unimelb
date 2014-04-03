# Print out term:freq dictionaries for a series of docids, from a
# shelve-based index.

# NOTE: it would be cleaner Python to create an "Index" object that
# abstracted many of these operations away.  Getting the interface to
# such an object correct requires some care, though, to distinguish
# indexes that are in parse, update, and query states.

if __name__ == '__main__':

    import sys
    import shelve

    if len(sys.argv) < 3:
        sys.stderr.write("USAGE: %s <db-file> <doc> ...\n" % sys.argv[0])
        sys.exit()
    index = shelve.open(sys.argv[1], 'r')  # Open for reading only

    # NOTE: a "shelve" object behaves very much like a standard Python
    # "dictionary".  You can, for instance, iterate over it, or get
    # its set of keys.

    for doc in sys.argv[2:]:
        freq_dict = index[doc]
        print("%s: %s" % (doc, freq_dict))
    index.close()
