#!/usr/bin/env python

import argparse
import os
import sys


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

    map = {}
    lexicon = {}

    with open(args.map, 'r') as map_file, open(args.lexicon, 'r') as lexicon_file:
        try:
            for line in map_file:
                (id, docno) = line.split()
                map[id] = docno
        except ValueError:
            print("Unable to parse <map> due to format error(s):")
            print("e.g. <id> <docno> -> 11 LA010189-0012")
            print("ERROR_LINE: " + line)
            sys.exit()

        try:
            for line in lexicon_file:
                (term, pointer) = line.split()
                lexicon[term] = pointer
        except ValueError:
            print("Unable to parse <lexicon> due to format error(s):")
            print("e.g. <term> <pointer> -> electricity 113")
            print("ERROR_LINE: " + line)
            sys.exit()

    with open(args.invlists) as i:
        try:
            for query in args.queries:
                byte_offset = int(lexicon[query])
                i.seek(byte_offset)
                inverted_list = i.next().rstrip().split()
                print(query)
                print(inverted_list[0])
                inverted_list_iterator = iter(inverted_list[1:])
                for item in inverted_list_iterator:
                    print(map[item] + ' '+ inverted_list_iterator.next() + '\n')
        except KeyError:
            print("No documents contain the query " + '<' + query + '>')
            sys.exit()


if __name__ == "__main__":
    main()