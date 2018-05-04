#!/usr/bin/env python

from math import log


class BM25:

    def __init__(self, k=1.2, b=0.75):
        """
        An algorithm that ranks documents in order of relevance from a query.

        :param k: a scoring constant, the default value is 1.2
        :param b: a scoring constant, the default value is 0.75
        """
        self.k = k
        self.b = b

    def weight(self, l, al):
        """
        Computes the value of 'K' in the BM25 score function.

        The function is dependant on the length of a document
        and the average length of documents within the collection.
        Thus, it is the document weighting function.

        :param l: the document length measured in bytes
        :param al: the average document length measured in bytes
        :return:
        """
        return self.k * ((1 - self.b) + ((self.b * l) / al))

    def score(self, n, f, d, w):
        """
        Computes the BM25 score for a single document given a term.

        :param n: the number of documents in the collection
        :param f: the number of documents containing the term
        :param d: the within-document frequency
        :param w: the document weight
        :return:
        """
        return log((n - f + 0.5) / (f + 0.5)) * (((self.k + 1) * d) / (w + d))
