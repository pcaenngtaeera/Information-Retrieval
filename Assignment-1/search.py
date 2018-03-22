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

    with open(args.map, 'r') as m, open(args.lexicon, 'r') as l:
        for line in m:
            (id, docno) = line.split()
            map[id] = docno
        for line in l:
            (term, pointer) = line.split()
            lexicon[term] = pointer

    with open(args.invlists) as i:
        for query in args.queries:
            if query in lexicon:
                byte_offset = int(lexicon[query])
                i.seek(byte_offset)
                inverted_list = i.next().rstrip().split()
                print(query)
                print(inverted_list[0])
                inverted_list_iterator = iter(inverted_list[1:])
                for item in inverted_list_iterator:
                    print(map[item] + ' '+ inverted_list_iterator.next() + '\n')
            else:
                print("No results found for query: " + '\'' + query + '\'')


if __name__ == "__main__":
    main()