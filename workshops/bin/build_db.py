
import os
import argparse
from workshops.lib.store.store import CollDataStore

def main():
    arg_parser=argparse.ArgumentParser(description='Build the lyrl tf-idf db.')
    arg_parser.add_argument('lyrl_path', type=str)
    arg_parser.add_argument('store_path', type=str)
    args=arg_parser.parse_args()
    CollDataStore(args.lyrl_path).dump(os.path.join(args.store_path, 'lyrl.db'))

if __name__ == '__main__':
    main()
