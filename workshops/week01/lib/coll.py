# Representation of an LYRL collection

class BowDoc:
    """Bag-of-words representation of a document.

    The document has an ID, and an iterable list of terms with their
    frequencies."""

    def __init__(self, docid):
        """Constructor.

        Set the ID of the document, and initiate an empty term dictionary.
        Call add_term to add terms to the dictionary."""
        # PYTHON NOTE: "self" is the name of the current object.  
        # You must pass "self" as the first argument to
        # each method call.
        #
        # One can freely create members of the object called FOO by assigning
        # to self.FOO.  Data members are not separately declared within
        # the class.  It is good form to initiate all object data members
        # in the constructor, even if only to "None".
        self.docid = docid
        self.terms = {}  # PYTHON NOTE: this is creating an empty dictionary

    def add_term(self, term_):
        """Add a term_ occurrence to the BOW representation.

        This should be called each time the term_ occurs in the document."""
        try:
            self.terms[term_] += 1
        # PYTHON NOTE: dictionaries raise a KeyError exception if you try
        # to access a key that doesn't exist
        except KeyError:  
            # PYTHON NOTE: this is accessing a field in the dictionary by key
            self.terms[term_] = 1

    def get_term_count(self, term_):
        """Get the term_ occurrence count for a term_.

        Returns 0 if the term_ does not appear in the document."""
        try:
            return self.terms[term_]
        except KeyError:
            return 0

    def get_term_list(self):
        """Get sorted list of all terms occurring in the document."""
        return sorted(self.terms.keys())

    def get_docid(self):
        """Get the ID of the document."""
        return self.docid

    def __iter__(self):
        """Return an ordered iterator over term--frequency pairs.

        Each element is a (term, frequency) tuple.  They are iterated
        in alphabetical order."""
        # PYTHON NOTE: iterators can be accessed and iterated using the syntax:
        #   "for element in object:"
        # See code at end of file.
        return iter(sorted(self.terms.items()))


class BowColl:
    """Collection of BOW documents."""

    def __init__(self):
        """Constructor.

        Creates an empty collection."""
        self.docs = {}

    def add_doc(self, doc_):
        """Add a document to the collection."""
        self.docs[doc_.get_docid()] = doc_

    def get_doc(self, docid):
        """Return a document by docid.

        Will raise a KeyError if there is no document with that ID."""
        return self.docs[docid]

    def get_docs(self):
        """Get the full list of documents.

        Returns a dictionary, with docids as keys, and docs as values."""
        return self.docs

    def inorder_iter(self):
        """Return an ordered iterator over the documents.
        
        The iterator will traverse the collection in docid order.  Modifying
        the collection while iterating over it leads to undefined results.
        Each element is a document; to find the id, call doc.get_docid()."""
        return BowCollInorderIterator(self)

    def get_num_docs(self):
        """Get the number of documents in the collection."""
        # PYTHON NOTE: len() returns the size of different collections,
        # including dictionaries, lists, and tuples.
        return len(self.docs)

    def __iter__(self):
        """Iterator interface.

        See inorder_iter."""
        # PYTHON NOTE: the __iter__ function is called behind the scenes
        # when we say "for element in object".
        return self.inorder_iter()

class BowCollInorderIterator:
    """Iterator over a collection."""
    # PYTHON NOTE: this illustrates how to write a Python iterator.  I
    # could have just sorted and returned the elements in inorder_iter()
    # above, but that would have involved creating a copy of the said
    # dictionary.  If you know a short-hand way of doing _precisely_ what
    # I want to do here (iterate over the items of a dictionary in key
    # order, but without actually returning the keys through the iterator),
    # let me know!

    def __init__(self, coll_):
        """Constructor.
        
        Takes the collection we're going to iterator over as sole argument."""
        self.coll = coll_
        self.keys = sorted(coll_.get_docs().keys())
        self.i = 0

    def __iter__(self):
        """Iterator interface."""
        return self

    def next(self):
        """Get next element."""
        # PYTHON NOTE: this is required to implement an iterator, and is
        # what actually gets called inside the "for element in object"
        # loop.  One raises StopIteration when the iterator has finished.
        if self.i >= len(self.keys):
            raise StopIteration
        doc_ = self.coll.get_doc(self.keys[self.i])
        self.i += 1
        return doc_

# PYTHON NOTE: this defines a top-level function, whereas "def" indented
# inside a class definition defines a method.
def parse_lyrl_coll(fname):
    """Parse an LYRL data file into a collection.

    Fname is the file name of the LYRL data file.  The parsed collection
    is returned.  NOTE the function performs very limited error checking."""
    # PYTHON NOTE: the next is an example of calling an object constructor.
    # The constructor is just the name of the class, invoked as a function.
    coll = BowColl()
    # PYTHON NOTE: "None" in Python is similar to "NULL" in C or C++.
    curr_doc = None
    # PYTHON NOTE: "for" loops work like this in Python: you iterate
    # over the object you want to look at the elements of.  When you use
    # "for" over an opened file descriptor (which is what open(fname) gives
    # us), it returns a line at a time from a file, as a string.
    #
    # If for some reason you do want to iterate over a sequence of
    # iterators, like in C, do:
    #     for i in range(0, 10):
    # NOTE: 0 is included in the range, but 10 is not.
    for line in open(fname):
        # PYTHON NOTE: strip leading and trailing space from a string.
        # I do this here primarily to strip off the trailing newline.
        line = line.strip()
        if line.startswith(".I"):
            # PYTHON NOTE: STRING.split() splits the string at whitespace,
            # and returns the result as a list.  I know that there are
            # going to be two elements in the list, so I can directly
            # assign them to two separate variables by saying 
            #   (var1, var2) = function_returning_list()
            # (Obviously, this is not robust error-checking code).
            (dot, docid) = line.split()
            curr_doc = BowDoc(docid)
        elif line.startswith(".W"):
            # PYTHON NOTE: "pass" means do nothing.  Because of Python's
            # indentation-based syntax, we have to put this in to let
            # the interpreter know this is an empty branch.
            pass  
        elif line == '':
            if curr_doc is not None:
                coll.add_doc(curr_doc)
            curr_doc = None
        else:
            terms = line.split()
            # PYTHON NOTE: terms is a list of the strings.  We iterate
            # over it like follows.
            for term_ in terms:
                curr_doc.add_term(term_)
    if curr_doc is not None:
        coll.add_doc(curr_doc)
    return coll

# PYTHON NOTE: the following line is a standard Python idiom.  It means
# that if we call this file as the main argument to the Python interpreter,
# the following code gets run.  However, if we import this file as a module
# to another file, the code doesn't get written.  This allows us to write
# file that can both be a standalone program, and provide functions to
# other programs.
if __name__ == '__main__':

    # PYTHON NOTE: "import" brings in another library, like "include"
    # in C or "import" in Java.  "sys" is a standard library.  Later, you'll
    # be importing this file into your other Python programs by placing it
    # in the same directory (or in directory in environmental variable
    # PYTHONPATH, if you want to get fancy), and then calling:
    #
    #     import coll
    #
    # Then you could call:
    #
    #     coll.parse_lyrl_coll()
    import sys

    # PYTHON NOTE: sys.argv contains the command-line arguments in a
    # list.  The first argument is the name of the program.  Note that
    # we say "sys.argv" to access the argv object inside the sys module.
    if len(sys.argv) != 2:
        # PYTHON NOTE: "%s" is a printf-like expression for formatting
        # a string inside another string.  The "%" operator (the second
        # one) performs this formatting directly, somewhat like:
        #    sprintf("%s", "foo")
        # in C.  If we had more than one format argument, we'd need
        # to put them in a tuple:
        #   "%s %d" % (string, int)
        sys.stderr.write("USAGE: %s <coll-file>\n" % sys.argv[0])
        sys.exit()
    coll = parse_lyrl_coll(sys.argv[1])

    for doc in coll:
        print(".D %s" % doc.get_docid())
        # PYTHON NOTE: as explained above, the iterator over BowDoc
        # returns _pairs_ of items (key, and value).  We unpack these
        # directly into their own variables
        for (term, freq) in doc:
            # PYTHON NOTE: syntax for multiple format arguments.
            print("%s:%d" % (term, freq))
        print("\n")
