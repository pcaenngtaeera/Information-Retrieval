#!/usr/bin/env python

from __future__ import division
from argparse import ArgumentParser
from heapq import heapify, heappush, heappop
from struct import unpack
from ranking import BM25
from time import time
from collection import Collection, tokenize
from math import factorial, pow, log
from itertools import repeat


def load_map(file_path):
    """
    Returns a map dictionary from a <map> file.

    The map dictionary has an 'id' of a document as the key.
    The value of each entry is a tuple of a 'docno' identifier
    and pre-calculated 'document_weight' for BM25 scoring.

    :param file_path: an absolute path to a <map> file
    :return: a map dictionary
    """
    map = {}
    with open(file_path, 'r') as map_file:
        for line in map_file:
            id, docno, weight = line.split()
            map[id] = (docno, float(weight))
    return map


def load_lexicon(file_path):
    """
    Returns a lexicon dictionary from a <lexicon> file.

    The lexicon dictionary has a 'term' as the key.
    The value of each entry is a 'byte_offset' of the term
    in the <invlists> file.

    :param file_path: an absolute path to a <lexicon> file
    :return: a lexicon dictionary
    """
    lexicon = {}
    with open(file_path, 'r') as lexicon_file:
        for line in lexicon_file:
            term, byte_offset = line.split()
            lexicon[term] = byte_offset
    return lexicon


def print_relevant_documents(query_label, relevant_documents):
    """
    Prints detail of the relevant documents starting with the highest ranked.

    The pre-condition requires the relevant documents to be in reverse order,
    i.e. the document with the lowest score is first. The precision of the score
    is truncated to 3 decimal places.

    :param query_label: a user-defined string to unique identify a query
    :param relevant_documents: a list of (score, docno) tuples with ascending scores
    :return:
    """
    for rank in range(1, len(relevant_documents) + 1):
        score, docno = relevant_documents[-rank]
        print("%s %s %d %.3f" % (query_label, docno, rank, score))


def accumulate_similarity_scores(query, lexicon, invlists, map):
    """
    Returns a dictionary of accumulated scores.

    The
    
    :param query: a list of terms
    :param lexicon: a lexicon dictionary
    :param invlists: an absolute path to a <invlists> file
    :param map: a map dictionary
    :param appended: a list of appended (term, )
    :return: 
    """
    document_scores = {}
    N = len(map)  # number of documents in the collection
    ranker = BM25()  # BM25 instance with default constants
    with open(invlists, 'rb') as invlists_file:
        for term in query:  # one term at a time
            if term in lexicon:  # term needs to exist in lexicon
                byte_offset = int(lexicon[term])  # address of term
                invlists_file.seek(byte_offset)  # move to address of term
                document_frequency = unpack('I', invlists_file.read(4))[0]  #
                for _ in repeat(None, document_frequency):  # iterate inverted list of term
                    docno, weight = map[str(unpack('I', invlists_file.read(4))[0])]  # get the docno
                    within_document_frequency = unpack('I', invlists_file.read(4))[0]  # get the within doc freq
                    if docno not in document_scores:  # create an accumulator for docno
                        document_scores[docno] = 0
                    document_scores[docno] += ranker.score(N, document_frequency, within_document_frequency, weight)
    return document_scores


def retrieve_top_ranked_documents(document_scores, R):
    """
    Returns a list of relevant documents in ascending similarity scores.

    Maintains a min-heap of (score, docno) tuples by adding the first 'num_results' documents.
    Pops the root until the heap is empty to retrieve the top re

    The number of documents return is not guaranteed to be equal to 'num_results'
    because a collection may contain less than 'num_results' relevant documents.

    :param document_scores: a dictionary of document scores
    :param R: the number of top-ranked documents that should be returned
    :return: a list of top-ranked documents
    """
    heap = []
    for docno, score in document_scores.iteritems():  # iterate accumulators
        if len(heap) < R:
            heappush(heap, (score, docno))
        else:  # heap is full
            if heap[0][0] < score:
                heap[0] = (score, docno)
                heapify(heap)
    return [heappop(heap) for _ in repeat(None, len(heap))]


def get_term_candidates(query, documents):
    """
    Returns a list of candidate terms for query expansion.

    Combines the terms in the relevant documents into a candidates list.
    Removes terms in the original query from the candidates.
    Stores the candidates in a set data structure to ensure uniqueness.

    :param query: a list of terms
    :param documents: a list of relevant Document objects
    :return: a set of candidate terms for query expansion
    """
    candidates = []
    for document in documents:
        candidates += document.terms
    return set([t for t in candidates if t not in query])


def accumulate_term_selection_values(lexicon, invlists, map, term_candidates, R, relevant_docnos):

    R_f = factorial(R)
    N = len(map)
    E = 25

    heap = []
    with open(invlists, 'rb') as invlists_file:
        for term in term_candidates:
            visited = []
            byte_offset = int(lexicon[term])  # address of term
            invlists_file.seek(byte_offset)  # move to address of term
            f_t = unpack('I', invlists_file.read(4))[0]  # frequency of term in collection
            r_t = 0  # frequency of term in relevant documents
            for _ in range(f_t):  # iterate inverted list of term
                docno = map[str(unpack('I', invlists_file.read(4))[0])][0]  # get the docno
                invlists_file.read(4)
                if docno in relevant_docnos and docno not in visited:
                    visited.append(docno)
                    r_t += 1

            # tsv calculation
            tsv = pow((f_t / N), r_t) * (R_f / (factorial(r_t) * factorial(R - r_t)))

            rsj = 0.3 * log(((r_t + 0.5) * (N - f_t - R + r_t + 0.5)) / ((f_t - r_t + 0.5) * (R - r_t + 0.5)))


            if len(heap) < E:
                heappush(heap, (-tsv, term, rsj))
            elif heap[0][0] < -tsv:
                heap[0] = (-tsv, term, rsj)
                heapify(heap)

    return [(heappop(heap)) for _ in range(len(heap))]


def additional_similarity_scores(document_scores, query, lexicon, invlists, map):
    """
    Returns a dictionary of accumulated scores.

    The

    :param query: a list of terms
    :param lexicon: a lexicon dictionary
    :param invlists: an absolute path to a <invlists> file
    :param map: a map dictionary
    :param appended: a list of appended (term, )
    :return:
    """
    ranker = BM25()  # BM25 instance with default constants
    with open(invlists, 'rb') as invlists_file:
        for q in query:  # one term at a time
            term, s = q
            byte_offset = int(lexicon[term])  # address of term
            invlists_file.seek(byte_offset)  # move to address of term
            document_frequency = unpack('I', invlists_file.read(4))[0]  #
            for _ in repeat(None, document_frequency):  # iterate inverted list of term
                docno, weight = map[str(unpack('I', invlists_file.read(4))[0])]  # get the docno
                within_document_frequency = unpack('I', invlists_file.read(4))[0]  # get the within doc freq
                if docno not in document_scores:  # create an accumulator for docno
                    document_scores[docno] = 0
                document_scores[docno] += ranker.score_aqe(s, within_document_frequency, weight)

    return document_scores

def main():
    """
    """
    # set up argument parser
    parser = ArgumentParser(add_help=False)
    parser.add_argument('-a', metavar="<algorithm>", required=True)
    parser.add_argument('-c', metavar="<collection>", required=True)
    parser.add_argument('-q', metavar="<query-label>", required=True)
    parser.add_argument('-n', metavar='<num-results>', required=True)
    parser.add_argument('-l', metavar='<lexicon>', required=True)
    parser.add_argument('-i', metavar='<invlists>', required=True)
    parser.add_argument('-m', metavar='<map>', required=True)
    parser.add_argument('-s', metavar='<stoplist>', nargs=1)
    parser.add_argument('query', metavar='<queryterm-1> [<queryterm-2> ... <queryterm-N>]', nargs='+')
    args = parser.parse_args()

    # begin timing
    start_time = time()

    # parse arguments
    algorithm = args.a
    if algorithm not in ('BM25','AQE'):
        exit("Unrecognized algorithm '" + args.a + "'. Recognized algorithms include 'BM25' and 'AQE'.")
    query_label = args.q
    num_results = int(args.n)
    map = load_map(args.m)
    invlists = args.i
    lexicon = load_lexicon(args.l)
    stoplist = args.s[0] if args.s else None
    query = tokenize(' '.join(args.query), stoplist)

    # print arguments (debug)

    # print("Algorithm: %s" % args.a)
    # print("Query: %s" % args.query)
    # print("Processed Query: %s" % query)
    # exit(0)

    # accumulate similarity scores

    document_scores = accumulate_similarity_scores(query, lexicon, invlists, map)

    #

    top_scores = retrieve_top_ranked_documents(document_scores, num_results)

    if algorithm == "BM25":
        print_relevant_documents(query_label, top_scores)

    elif algorithm == "AQE":

        relevant_docnos = []
        c = Collection(args.s[0]) if args.s else Collection()
        for top in top_scores:
            docno = top[1]
            relevant_docnos.append(docno)
            c.parse_document(args.c, docno)

        term_candidates = get_term_candidates(query, c.documents)

        top_E_terms = accumulate_term_selection_values(lexicon, invlists, map, term_candidates, len(top_scores), relevant_docnos)

        additional_terms = []
        for top in top_E_terms:
            additional_terms.append((top[1], top[2]))

        new = additional_similarity_scores(document_scores, additional_terms, lexicon, invlists, map)

        top_scores = retrieve_top_ranked_documents(new, num_results)
        print_relevant_documents(query_label, top_scores)



    print("\nRunning time: %d ms" % ((time() - start_time) * 1000))

if __name__ == "__main__":
    main()
