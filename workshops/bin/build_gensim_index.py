
import argparse
from workshops.lib.store.gensim_index import make_index

def main():
    arg_parser=argparse.ArgumentParser(description='Build the lyrl gensim db.')
    arg_parser.add_argument('lyrl_fname', type=str)
    arg_parser.add_argument('index_tag', type=str)
    args = arg_parser.parse_args()
    make_index(args.lyrl_fname, args.gsindex_tag)

if __name__ == '__main__':
    main()
