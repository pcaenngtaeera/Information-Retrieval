#!/usr/bin/env python

from argparse import ArgumentParser


def main():
    """
    """
    parser = ArgumentParser(add_help=False)
    parser.add_argument('-BM25', action='store_true', required=True)
    parser.add_argument('-q', metavar="<query-label>", required=True)
    parser.add_argument('-n', metavar='<num-results>', required=True)
    parser.add_argument('-l', metavar='<lexicon>', required=True)
    parser.add_argument('-i', metavar='<invlists>', required=True)
    parser.add_argument('-m', metavar='<map>', required=True)
    parser.add_argument('-s', metavar='<stoplist>')
    parser.add_argument('queryterms', metavar='<queryterm-1> [<queryterm-2> ... <queryterm-N>]', nargs='+')
    args = parser.parse_args()

if __name__ == "__main__":
    main()
