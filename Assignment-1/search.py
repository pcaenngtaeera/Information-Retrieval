#!/usr/bin/env python

import argparse
import os


map = {}
lexicon = {}


def is_file(path):
    if os.path.isfile(path):
        return path
    else:
        raise argparse.ArgumentTypeError("unable to load file at " + path)


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('lexicon', metavar='<lexicon>', type=is_file)
    parser.add_argument('invlists', metavar='<invlists>', type=is_file)
    parser.add_argument('map', metavar='<map>', type=is_file)
    parser.add_argument('queries', metavar='<queryterm>', nargs='+')
    args = parser.parse_args()

    with open('map', 'r') as m, open('lexicon', 'r') as l:
        for line in m:
            (id, docno) = line.split()
            map[int(id)] = docno
        for line in l:
            (term, pointer) = line.split()
            lexicon[term] = pointer


if __name__ == "__main__":
    main()