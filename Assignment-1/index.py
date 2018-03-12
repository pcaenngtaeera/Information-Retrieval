#!/usr/bin/env python
import argparse
import os
import sys
from document_parser import *

def is_file(path):
    if os.path.isfile(path):
        return path
    else:
        raise argparse.ArgumentTypeError("Unable to load file at " + path)

def main():
    parser = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
    parser.add_argument('-s', metavar = '\b <stopfile>', nargs=1, type=is_file)
    parser.add_argument('-p', action='store_true')
    parser.add_argument('sourcefile', metavar = '<sourcefile>', type=is_file)
    args = parser.parse_args()

    with open(args.sourcefile, 'r') as f:
        dp = document_parser(f.read())
        if args.s:
            dp.apply_stoplist(args.s[0])
        dp.extract_documents()
        dp.map_to_disk()
        if args.p:
            dp.print_terms()
    f.close()

if __name__ == "__main__":
    main()


