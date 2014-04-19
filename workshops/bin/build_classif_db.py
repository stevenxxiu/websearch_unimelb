
import os
import argparse
from workshops.lib.store.store import CollDataStore
from workshops.lib.store.classif import LyrlClassifDataStore

def main():
    arg_parser=argparse.ArgumentParser(description='Build the lyrl classif db.')
    arg_parser.add_argument('lyrl_path', type=str)
    arg_parser.add_argument('store_path', type=str)
    args=arg_parser.parse_args()
    LyrlClassifDataStore(args.lyrl_path, CollDataStore.load(os.path.join(args.store_path, 'lyrl.db')))\
        .dump(os.path.join(args.store_path, 'lyrl_classif.db'))

if __name__ == '__main__':
    main()
