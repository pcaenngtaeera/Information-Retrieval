#!/usr/bin/env python

import argparse
import os
import struct
import time


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

    start = time.time()

    map = {}
    lexicon = {}

    with open(args.map, 'r') as map_file, open(args.lexicon, 'r') as lexicon_file:
        for line in map_file:
            (id, docno) = line.split()
            map[int(id)] = docno
        for line in lexicon_file:
            (term, pointer) = line.split()
            lexicon[term] = pointer

    with open(args.invlists, 'rb') as invlists_file:
            for query in args.queries:
                if query in lexicon:
                    print(query)
                    byte_offset = int(lexicon[query])
                    invlists_file.seek(byte_offset)
                    inverted_list_count = struct.unpack('I', invlists_file.read(4))[0]
                    print(inverted_list_count)
                    for i in range(inverted_list_count):
                        docno = map[struct.unpack('I', invlists_file.read(4))[0]]
                        count = str(struct.unpack('I', invlists_file.read(4))[0])
                        print(docno + ' ' + count)

    print(time.time() - start)


if __name__ == "__main__":
    main()