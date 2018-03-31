#!/usr/bin/env python

import argparse
import re
import struct
from collections import Counter


class Document:
    def __init__(self, id, docno, terms):
        self.id = id
        self.docno = docno
        self.terms = terms


class Collection:
    def __init__(self, sourcefile, stoplist):
        self.documents = []
        self.parse_documents(sourcefile, stoplist)

    def parse_documents(self, sourcefile, stoplist):
        id = 0
        docno = ''
        contents = ''
        in_headline_text = False
        if stoplist:
            with open(stoplist[0], 'r') as f:
                stoplist = set(f.read().split('\n'))
        with open(sourcefile, 'r') as f:
            term_regex = re.compile('[^a-zA-Z-/\']')
            for line in f:
                if line == '<TEXT>\n' or line == '<HEADLINE>\n':
                    in_headline_text = True
                elif line == '</TEXT>\n' or line == '</HEADLINE>\n':
                    in_headline_text = False
                elif in_headline_text and not line.startswith(('<', '</')):
                    contents += line
                elif line.startswith('<DOCNO'):
                    docno = line[8:-10]
                elif line == '<DOC>\n':
                    contents = ''
                elif line == '</DOC>\n':
                    id += 1
                    terms = []
                    words = term_regex.sub(' ', contents).lower().split()
                    for word in words:
                        if word.isalpha():
                            terms.append(word)
                        elif '-' in word:
                            terms.extend(word.split('-'))
                        elif '/' in word:
                            terms.extend(word.split('/'))
                        elif '\'' in word:
                            terms.extend(word.split('\''))
                    if stoplist:
                        terms = [t for t in terms if t not in stoplist]
                    self.documents.append(Document(id, docno, terms))

    def print_terms(self):
        for document in self.documents:
            for term in document.terms:
                print(term)

    def write_map_to_disk(self):
        with open('map', 'w+') as f:
            for document in self.documents:
                f.write(str(document.id) + ' ' + document.docno + '\n')

    def write_inverted_list_to_disk(self):
        postings = {}
        if self.documents:
            for document in self.documents:
                for term in document.terms:
                    if term in postings:
                        postings[term].append(document.id)
                    else:
                        postings[term] = [document.id]

        with open('invlists', 'wb') as invlists_file, open('lexicon', 'w') as lexicon_file:
            for term in postings.keys():
                lexicon_file.write(term + ' ' + str(invlists_file.tell()) + '\n')
                term_counts = Counter(postings[term])
                invlists_file.write(str(struct.pack('I', len(term_counts.keys()))))
                for document_id in term_counts.keys():
                    invlists_file.write(struct.pack('II', document_id, term_counts[document_id]))


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-s', metavar='\b <stopfile>', nargs=1)
    parser.add_argument('-p', action='store_true')
    parser.add_argument('sourcefile', metavar='<sourcefile>')
    args = parser.parse_args()

    collection = Collection(args.sourcefile, args.s)
    collection.write_map_to_disk()
    collection.write_inverted_list_to_disk()
    if args.p:
        collection.print_terms()

if __name__ == "__main__":
    main()
