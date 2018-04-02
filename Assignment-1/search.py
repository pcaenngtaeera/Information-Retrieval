#!/usr/bin/env python

import argparse
import itertools
import struct


def main():
    """

    <search.py> requires 3 files as an argument and a number of space-separated queries (n >= 1).
    The <lexicon> and <map> files are loaded into dictionaries for faster access.
    Iterating the list of queries, it outputs the following if the query exists in the <lexicon>:

        > [query_1]
        > [document_count]
        > [document_1_docno] [document_1_query_count]
        > ...
        > ...
        > ...
        > [document_n] [document_n_query_count]

    <invlists> is accessed using a byte-offset in the <lexicon> with the query as the key.
    The inverted list is found by seeking to the byte-offset of the document frequency.
    This is followed by an equal number of <docno> identifier and within-document frequency pairs.
    This information is printed to the console in the aforementioned format.

    :collection_map: a dictionary with <id> as the key and <docno> as the value
    :token_lexicon: a dictionary with <token> as the key and <pointer> as the value
    :invlists_file: a binary integer file (32-bit integers)

    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('lexicon', metavar='<lexicon>')
    parser.add_argument('invlists', metavar='<invlists>')
    parser.add_argument('map', metavar='<map>')
    parser.add_argument('queries', metavar='<queryterm>', nargs='+')
    args = parser.parse_args()

    collection_map = {}
    token_lexicon = {}

    with open(args.map, 'r') as map_file, open(args.lexicon, 'r') as lexicon_file:
        for line in map_file:
            (id, docno) = line.split()
            collection_map[int(id)] = docno
        for line in lexicon_file:
            (token, pointer) = line.split()
            token_lexicon[token] = pointer

    with open(args.invlists, 'rb') as invlists_file:
            for query in args.queries:
                if query in token_lexicon:
                    print(query)
                    invlists_file.seek(int(token_lexicon[query]))
                    document_frequency = struct.unpack('I', invlists_file.read(4))[0]
                    print(document_frequency)
                    for _ in itertools.repeat(None, document_frequency):
                        print(collection_map[struct.unpack('I', invlists_file.read(4))[0]] + ' ' + str(struct.unpack('I', invlists_file.read(4))[0]))


if __name__ == "__main__":
    main()
