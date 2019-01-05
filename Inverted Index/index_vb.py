#!/usr/bin/env python

from argparse import ArgumentParser
from collection import Collection


def main():
    """
    <index.py> requires a path to a <collection> as an argument.

    The required "sourcefile" argument is a path to a <collection>
    The optional "-s" argument requires a path to a <stoplist> as an extra argument.
    The optional "-p" argument is a Boolean switch
    """
    parser = ArgumentParser(add_help=False)
    parser.add_argument('-s', metavar='\b <stopfile>', nargs=1)
    parser.add_argument('-p', action='store_true')
    parser.add_argument('sourcefile', metavar='<sourcefile>')
    args = parser.parse_args()

    collection = Collection(args.sourcefile, args.s[0]) if args.s else Collection(args.sourcefile)
    collection.write_map_to_disk()
    collection.write_compressed_invlists_lexicon_to_disk()
    if args.p:
        collection.print_terms()


if __name__ == "__main__":
    main()
