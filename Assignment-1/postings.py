#!/usr/bin/env python

import struct


class Postings:
    def __init__(self, collection):
        self.postings = {}
        if collection.documents:
            for document in collection.documents:
                for term in document.terms:
                    if term in self.postings:
                        if document.id in self.postings[term]:
                            self.postings[term][document.id] += 1
                        else:
                            self.postings[term][document.id] = 1
                    else:
                        self.postings[term] = {document.id: 1}

    def generate_inverted_index(self):
        with open('invlists', 'wb') as invlists_file, open('lexicon', 'w') as lexicon_file:
            for term in self.postings.keys():
                lexicon_file.write(term + ' ' + str(invlists_file.tell()) + '\n')
                invlists_file.write(str(struct.pack('I', len(self.postings[term].keys()))))
                for document_id in self.postings[term].keys():
                    invlists_file.write(struct.pack('II', document_id, self.postings[term][document_id]))
