#!/usr/bin/env python

from math import log

k = 1.2
b = 0.75


def BM25_K(L, AL):
    """
    Computes the value of K in the BM25 similarity function.

    :param L: the document length measured in bytes
    :param AL: the average document length measured in bytes
    :return: the computed value of K in BM25
    """
    return k * ((1 - b) + ((b * L) / AL))


def BM25_Similarity(Q, D, AL):
    """
    Computes the similarity

    :param Q: the query consisting of terms
    :param D: a document in the collection
    :param AL: the average document length measured in bytes
    :return: the computed BM25 similarity score
    """

    L = 0  # the document length measured in bytes
    N = 0  # the number of documents in the collection

    score = 0
    for t in Q:
        f = 0  # the number of documents containing 't'
        o = 0  # the number of occurences of 't' in 'D'
        score += log((N - f + 0.5) / (f + 0.5)) * (((k + 1) * o) / (BM25_K(L, AL) * o))

    return score
