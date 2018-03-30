#!/usr/bin/env python

import re
from document import Document

markup_pattern = re.compile('<(.*?)>')
word_pattern = re.compile('[^a-zA-Z-/]')


class Collection:
    def __init__(self):
        self.stoplist = {}
        self.documents = []

    def get_documents(self, sourcefile):
        id = 0
        text = ''
        with open(sourcefile, 'r') as f:
            for line in f:
                if line == '<DOC>\n':
                    text = ''
                elif line == '</DOC>\n':
                    self.documents.append(self.parse_document(id, text))
                    id += 1
                else:
                    text += line

    def get_terms(self, text):
        terms = []
        words = markup_pattern.sub('', text).split()
        for term in words:
            word = word_pattern.sub('', term).lower()
            if word.isalpha():
                terms.append(word)
            elif '-' in word: # hyphenated word
                h_words = word.split('-')
                for h_word in h_words:
                    terms.append(h_word)
            elif '/' in word: # slash word
                s_words = word.split('/')
                for s_word in s_words:
                    terms.append(s_word)
        if self.stoplist:
            return [t for t in terms if t not in self.stoplist]
        else:
            return terms

    def parse_document(self, id, text):
        lines = text.split('\n')
        docno = lines[0][8:-9]
        n, s, e = 0, 0, 0
        markers = []
        for line in lines:
            if line == '<TEXT>' or line == '<HEADLINE>':
                s = n
            elif line == '</TEXT>' or line == '</HEADLINE>':
                e = n
                markers.append((s, e))
            n += 1
        terms = []
        for marker in markers:
            terms += lines[marker[0]:marker[1]]
        terms = self.get_terms(' '.join(terms))
        return Document(id, docno, terms)

    def use_stoplist(self, path):
        with open(path, 'r') as f:
            self.stoplist = set(f.read().split('\n'))

    def map_to_disk(self):
        with open('map', 'w+') as f:
            for document in self.documents:
                f.write(str(document.id) + ' ' + document.docno + '\n')

    def print_terms(self):
        for document in self.documents:
            document.print_terms()
