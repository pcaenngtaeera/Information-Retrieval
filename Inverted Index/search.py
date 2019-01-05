#!/usr/bin/env python

import argparse
import itertools
import struct


def main():
    """

    <search.py> requires 3 files as an argument and a number of space-separated queries (n >= 1).
    The <lexicon> and <map> files are loaded into a dictionaries for faster access.
    The list of queries is iterated, outputting the following if the query exists in the lexicon:

        > [query_1]
        > [document_count]
        > [document_1_docno] [document_1_query_count]
        > ...
        > ...
        > ...
        > [document_n] [document_n_query_count]

    An inverted list from <invlists> is directly accessed by using a byte-offset found in the lexicon.
    The inverted list is begins with the <document frequency>, to indicate the size of the list.
    It is followed by an equal number of <docno> and <within-document frequency> pairs.
    This information is printed to the console in a list using the above format.

    The conversion from binary integers to integers is handled by the <struct> library.
    <struct> treats every 4 bytes (32 bits) from the <byte_offset> as an integer.

    ---

    :local document_map: a dictionary with document <id> as the key and <docno> as the value
    :local term_lexicon: a dictionary with <term> as the key and <byte_offset> as the value
    :local invlists_file: a binary integer file (32-bit integers)

    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('lexicon', metavar='<lexicon>')
    parser.add_argument('invlists', metavar='<invlists>')
    parser.add_argument('map', metavar='<map>')
    parser.add_argument('queryterms', metavar='<queryterm>', nargs='+')
    args = parser.parse_args()

    document_map = {}
    term_lexicon = {}

    with open(args.map, 'r') as map_file, open(args.lexicon, 'r') as lexicon_file:
        for line in map_file:
            (id, docno) = line.split()
            document_map[id] = docno
        for line in lexicon_file:
            (term, byte_offset) = line.split()
            term_lexicon[term] = byte_offset

    with open(args.invlists, 'rb') as invlists_file:
        for term in args.queryterms:
            if term in term_lexicon:
                print(term)
                byte_offset = int(term_lexicon[term])
                invlists_file.seek(byte_offset)  # sets the file's current position to the offset
                document_frequency = struct.unpack('I', invlists_file.read(4))[0]
                print(document_frequency)
                for _ in itertools.repeat(None, document_frequency):
                    docno = document_map[str(struct.unpack('I', invlists_file.read(4))[0])]
                    within_document_frequency = str(struct.unpack('I', invlists_file.read(4))[0])
                    print(docno + ' ' + within_document_frequency)


if __name__ == "__main__":
    main()
