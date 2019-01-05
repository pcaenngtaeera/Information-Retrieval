#!/usr/bin/env python

from argparse import ArgumentParser
from compression import decode


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
    <struct> treats every 4 bytes (32 bit) from the <byte_offset> as an integer.
    """
    parser = ArgumentParser(add_help=False)
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
                invlists_file.seek(byte_offset)
                document_frequency = decode(invlists_file)
                print(document_frequency)
                for _ in range(document_frequency):
                    docno = document_map[str(decode(invlists_file))]
                    within_document_frequency = str(decode(invlists_file))
                    print(docno + ' ' + within_document_frequency)


if __name__ == "__main__":
    main()
