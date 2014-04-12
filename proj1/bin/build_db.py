
import os
import argparse
from proj1.lib.store import WikiDataStore, ApacheDataStore

def main():
    arg_parser=argparse.ArgumentParser(description='Build the wiki tf-idf db.')
    arg_parser.add_argument('wiki_path', type=str)
    arg_parser.add_argument('apache_path', type=str)
    arg_parser.add_argument('store_path', type=str)
    args=arg_parser.parse_args()
    # we use separate collections for wikipedia and the apache forum, as the document lengths and term occurances likely differ
    WikiDataStore(args.wiki_path).dump(os.path.join(args.store_path, 'wiki.db'))
    ApacheDataStore(args.apache_path).dump(os.path.join(args.store_path, 'apache.db'))

if __name__ == '__main__':
    main()
