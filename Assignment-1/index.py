#!/usr/bin/env python
import sys
import argparse
import os

# check if file exists at path
def is_file(path):
    if os.path.isfile(path):
        return path
    else:
        raise argparse.ArgumentTypeError("unable to load file")

# main
def main():

    # argument parser
    parser = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
    parser.add_argument('-s', metavar = '\b <stopfile>', nargs=1, type=is_file)
    parser.add_argument('-p', action='store_true')
    parser.add_argument('sourcefile', metavar = '<sourcefile>', type=is_file)

    # parse arguments
    args = parser.parse_args() 
    if args.sourcefile: # unnecessary check, here for readability
        print("loaded sourcefile")
        if args.s:
            print('-s option enabled + stopfile at: ' + args.s[0])
        if args.p:
            print('-p option enabled')

if __name__ == "__main__":
    main()

