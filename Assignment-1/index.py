#!/usr/bin/env python

import argparse
import os
from collection import Collection


def is_file(path):
    if os.path.isfile(path):
        return path
    else:
        raise argparse.ArgumentTypeError("unable to load file at " + path)


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-s', metavar='\b <stopfile>', nargs=1, type=is_file)
    parser.add_argument('-p', action='store_true')
    parser.add_argument('sourcefile', metavar='<sourcefile>', type=is_file)
    args = parser.parse_args()
    collection = Collection()
    if args.s:
        collection.use_stoplist(args.s[0])
    collection.get_documents(args.sourcefile)
    collection.map_to_disk()
    if args.p:
        collection.print_terms()
    collection.generate_inverted_index()


if __name__ == "__main__":
    main()
