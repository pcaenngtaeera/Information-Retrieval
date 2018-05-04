#!/usr/bin/env python

from collections import Counter
from ranking import BM25
from re import compile, split
from struct import pack


class Document:

    def __init__(self, id, docno, terms):
        """
        Contains the identifiers and terms found within a document.

        Includes the length of the document as the combined length of each term.
        Using the invariant that the terms only contains the alphabet,
        we assume that each character is equal to 1 byte in UTF-8 encoding.
        Hence, the length of a document is the number of indexed bytes.

        :param id: an incremental identifier assigned to each document
        :param docno: an identifier parsed from [<DOCNO></DOCNO>]
        :param terms: a list of terms in order of discovery
        """
        self.id = id
        self.docno = docno
        self.terms = terms
        self.length = sum(map(len, terms))


class Collection:

    def __init__(self, sourcefile, stoplist=None):
        """
        Contains functions to index a collection.

        :param sourcefile: a path to a collection
        :param stoplist: an optional path to a stoplist
        """
        self.stoplist = None
        if stoplist:
            with open(stoplist, 'r') as f:
                self.stoplist = set(f.read().split('\n'))
        self.documents = []
        self.parse_collection(sourcefile)

    def tokenize_terms(self, words):
        """
        Converts a list of words into terms based on a set of rules/

        We decided to keep words containing either hyphens, forward-slashes or apostrophes
        in our earlier regex because they themselves are composed of multiple words.
        We now use another another regex that matches word groups to extract the words.

        The reasoning behind these decisions is to maintain the structure of the words.
        This is so the index reflects what a typical user expects. For example in a search
        function where the user wants to find occurrences of "campus", it is preferable to
        recognize "on-campus" as a legitimate source of "campus".

        :param words: a list of words before tokenization
        :return terms: a list of words after tokenization
        """
        terms = []
        for word in words:
            if word.isalpha():
                terms.append(word)
            else:
                terms.extend(split('\W+', word))
        if self.stoplist:
            terms = [t for t in terms if t not in self.stoplist]
        return terms

    def parse_collection(self, sourcefile):
        """
        Iterates the <collection> one line at time to store important data.

        > begin <appending> if line equals "<TEXT>" or "<HEADLINE>"
        > stop <appending> if line equals "</TEXT>" or "</HEADLINE>"
        > appends the line to <content> if <appending> and not a tag ELSE
        > assigns <docno> if it encounters a <DOCNO></DOCNO> tag ELSE
        > resets <content> if line equals "<DOC>"
        > tokenizes <content> if line equals "</DOC>" and increments <id>

        :param sourcefile: a path to a <collection>
        """
        with open(sourcefile, 'r') as f:
            id = 0
            docno = ''
            content = ''
            appending = False
            term_regex = compile('[^a-zA-Z-/\']')
            for line in f:
                if line == '<TEXT>\n' or line == '<HEADLINE>\n':
                    appending = True
                elif line == '</TEXT>\n' or line == '</HEADLINE>\n':
                    appending = False
                elif appending and not line.startswith(('<', '</')):
                    content += line
                elif line.startswith('<DOCNO>'):
                    docno = line[8:-10]
                elif line == '<DOC>\n':
                    content = ''
                elif line == '</DOC>\n':
                    id += 1
                    terms = self.tokenize_terms(term_regex.sub(' ', content).lower().split())
                    self.documents.append(Document(id, docno, terms))

    def write_map_to_disk(self):
        """
        Writes a <map> file to the current working directory.

        The <map> file is line-separated, where each line consists of '<id> <docno> <document_weight>'.
        The <document_weight> is calculated as the value of K in BM25's scoring function.
        """
        al = sum(map(lambda d: d.length, self.documents)) / len(self.documents)
        ranker = BM25()
        with open('map', 'w') as f:
            for document in self.documents:
                f.write(str(document.id) + ' ' + document.docno + ' ' + str(ranker.weight(document.length, al)) + '\n')

    def create_postings(self):
        """
        Builds a dictionary for the term occurrence statistics of the Collection.

        :return postings: a dictionary with "term" as a key and a list of Document "id" as a value
        """
        postings = {}
        if self.documents:
            for document in self.documents:
                for term in document.terms:
                    if term in postings:
                        postings[term].append(document.id)
                    else:
                        postings[term] = [document.id]
        return postings

    def write_invlists_lexicon_to_disk(self):
        """
        Writes an <invlists> file and <lexicon> file to the current working directory.

        <invlists> is a binary integer file (32-bit) composed of sequential inverted lists.
        Each inverted list is preceded by a document frequency integer.
        This is followed by an number of "<id> <token_frequency>" pairs equal to the document frequency.
        <lexicon> is a key-value-pair where every "key" is "term" that is assigned a byte-offset from <tell>.
        The order of terms/documents in <invlists> and <lexicon> are unordered because <postings> is unordered.
        """
        postings = self.create_postings()
        with open('invlists', 'wb') as invlists_file, open('lexicon', 'w') as lexicon_file:
            for term in postings.keys():
                lexicon_file.write(term + ' ' + str(invlists_file.tell()) + '\n')  # gets the position of the file
                term_occurrences = Counter(postings[term])  # tallies term occurrences by document <id>
                document_frequency = len(term_occurrences.keys())
                invlists_file.write(str(pack('I', document_frequency)))
                for document_id in term_occurrences.keys():
                    invlists_file.write(pack('II', document_id, term_occurrences[document_id]))
