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

    def document_weight(self, l, al):
        """
        Computes the value of 'K' in the BM25 score function.

        The function is dependant on the length of a document
        and the average length of documents within the collection.
        Thus, it is independant from the statistics of a term.

        :param l: the document length measured in bytes
        :param al: the average document length measured in bytes
        :return:
        """
        return self.k * ((1 - self.b) + ((self.b * l) / al))

    def score(self, N, f_t, d, w):
        """
        Computes the BM25 score for a single document given a term.

        By default the equation uses the inverse document frequency (IDF)
        to calculate the weight for a term.

        :param N: the number of documents in the collection
        :param f_t: the number of documents containing the term
        :param d: the within-document frequency
        :param w: the document weight
        :param m: optional multiplier used in query expansion
        :return:
        """
        return log((N - f_t + 0.5) / (f_t + 0.5)) * (((self.k + 1) * d) / (w + d))

    def score_aqe(self, s, d, w):
        """
        Computes the BM25 score for a single document given a term.

        By default the equation uses the inverse document frequency (IDF)
        to calculate the weight for a term.

        :param N: the number of documents in the collection
        :param f_t: the number of documents containing the term
        :param d: the within-document frequency
        :param w: the document weight
        :param m: optional multiplier used in query expansion
        :return:
        """
        return s * (((self.k + 1) * d) / (w + d))

    def idf_term_weight(self):
        return
