#!/usr/bin/env python

import argparse
import re
import struct
from collections import Counter


class Document:
    def __init__(self, id, docno, terms):
        """

        A class holding the important information of a <document> within the <collection>.

        ---

        :param id: an incremental identifier assigned to each document
        :param docno: an identifier parsed from [<DOCNO></DOCNO>]
        :param terms: a list of terms in order of discovery

        """
        self.id = id
        self.docno = docno
        self.terms = terms


class Collection:
    def __init__(self, sourcefile, stoplist=None):
        """

        A class which parses a <collection> and and saves the relevant information in a group of <document>.
        Contains functions to write index-associated files to disk, and print terms to <stdout>.

        ---

        :param _documents: a private list of documents
        :param _stoplist: a private set of words to be ignored during the indexing process(optional)

        """
        if stoplist:
            with open(stoplist, 'r') as f:
                self._stoplist = set(f.read().split('\n'))
        else:
            self._stoplist = {}
        self._documents = []
        self._parse_collection(sourcefile)

    def print_terms(self):
        """

        Prints the terms of each document from the collection to <stdout> (in-order).

        """
        for document in self._documents:
            for term in document.tokens:
                print(term)

    def write_map_to_disk(self):
        """

        Writes a <map> file to the current working directory.

        <map> is line-separated '<id> <docno>' written in order of appearance.
        <map> is used to retrieve a <docno> from a document <id>.

        """
        with open('map', 'w') as f:
            for document in self._documents:
                f.write(str(document.id) + ' ' + document.docno + '\n')

    def write_invlists_to_disk(self):
        """

        Writes an <invlists> file and <lexicon> file to the current working directory.

        <invlists> is a binary integer file (32 bit) composed of sequential inverted lists.
        Each inverted list is preceded by a document frequency integer.
        This is followed by an number of '<id> <token_frequency>' pairs equal to the document frequency.

        <lexicon> is a key-value-pair where every term is assigned a byte-offset from <tell>.
        Because the <postings> is a dictionary the contents are unordered, hence <invlists> and <lexicon> are too.

        """
        postings = self._build_postings()
        with open('invlists', 'wb') as invlists_file, open('lexicon', 'w') as lexicon_file:
            for term in postings.keys():
                lexicon_file.write(term + ' ' + str(invlists_file.tell()) + '\n')  # gets the position of the file
                term_occurences = Counter(postings[term])  # tallies term occurences by document <id>
                document_frequency = str(struct.pack('I', len(term_occurences.keys())));
                invlists_file.write(document_frequency)
                for document_id in term_occurences.keys():
                    invlists_file.write(struct.pack('II', document_id, term_occurences[document_id]))

    def _build_postings(self):
        """
        Builds a dictionary that contains the frequency information of each token in <documents>.
        The frequency is in the form of a list of <id> in which a given token appears

        :return postings: a dictionary with <token> as the key and a list of document <id> as the value
        """
        postings = {}
        if self._documents:
            for document in self._documents:
                for token in document.tokens:
                    if token in postings:
                        postings[token].append(document.id)
                    else:
                        postings[token] = [document.id]
        return postings

    def _parse_collection(self, sourcefile):
        """

        Iterates the <collection> one line at time and starting with an empty <contents>:

            > stops <appending> if it encounters a relevant tag ELSE
            > starts <appending> if it encounters a relevant tag ELSE
            > appends the line to <contents> if <appending> and not a tag ELSE
            > sets <docno> if it encounters a <DOCNO></DOCNO> tag ELSE
            > resets <contents> if it encounters the beginning of a document
            > tokenize <contents> if it reaches the end of a document

        ---

        :param sourcefile: a string of the path to a <collection> file

        :local appending: a Boolean that checks whether we are inside an appropriate tag
        :local term_regex: a pre-compiled regex which defines alphabetical words (including have - or / or ')

        """
        with open(sourcefile, 'r') as f:
            id = 0
            docno = ''
            contents = ''
            appending = False
            term_regex = re.compile('[^a-zA-Z-/\']')
            for line in f:
                if line == '<TEXT>\n' or line == '<HEADLINE>\n':
                    appending = True
                elif line == '</TEXT>\n' or line == '</HEADLINE>\n':
                    appending = False
                elif appending and not line.startswith(('<', '</')):
                    contents += line
                elif line.startswith('<DOCN'):
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
                    if self._stoplist:
                        terms = [t for t in terms if t not in self._stoplist]
                    self._documents.append(Document(id, docno, terms))


def main():
    """

    <index.py> requires a path to a <collection> as an argument.
    The optional -s argument requires a path to a <stoplist> as an argument.
    The optional -p argument prints every token in-order to <stdout>

    ---

    :local collection: a custom class which houses documents and operates on them

    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-s', metavar='\b <stopfile>', nargs=1)
    parser.add_argument('-p', action='store_true')
    parser.add_argument('sourcefile', metavar='<sourcefile>')
    args = parser.parse_args()

    collection = Collection(args.sourcefile, args.s[0]) if args.s else Collection(args.sourcefile)
    collection.write_map_to_disk()
    collection.write_invlists_to_disk()
    if args.p:
        collection.print_terms()


if __name__ == "__main__":
    main()
