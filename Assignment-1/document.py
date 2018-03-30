#!/usr/bin/env python

class Document:
    def __init__(self, id, docno, terms):
        self.id = id
        self.docno = docno
        self.terms = terms

    def print_terms(self):
        for term in self.terms:
            print(term)
