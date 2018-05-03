#!/usr/bin/env python

from math import log


class BM25:

    def __init__(self, n, al, k=1.2, b=0.75):
        """
        An algorithm that ranks documents in order of relevance to a given query.

        :param n: the number of documents in the collection
        :param al: the average length of documents in the collection
        :param k: a scoring constant, the default value is 1.2
        :param b: a scoring constant, the default value is 0.75
        """
        self.n = n
        self.al = al
        self.k = k
        self.b = b

    def weight(self, l):
        """
        Computes the value of 'K' in the BM25 score function.

        The function is dependant on the length of a document
        and the average length of documents within the collection.
        Thus, it is the document weighting function.

        :param l: the document length measured in bytes
        :return:
        """
        return self.k * ((1 - self.b) + ((self.b * l) / self.al))

    def score(self, q, d):
        """
        Computes the BM25 score for a document given a query.

        :param q: the query comprising of a list of terms
        :param d: the document
        :return:
        """
        score = 0
        for t in q:
            score += log((self.n - d.f + 0.5) / (d.f + 0.5)) * (((self.k + 1) * d.o) / (d.w * d.o))
        return score
