#!/usr/bin/env python

from argparse import ArgumentParser
from heapq import *
from struct import unpack
from ranking import BM25
from time import time


def main():
    """
    """
    parser = ArgumentParser(add_help=False)
    parser.add_argument('-BM25', action='store_true', required=True)
    parser.add_argument('-q', metavar="<query-label>", required=True)
    parser.add_argument('-n', metavar='<num-results>', required=True)
    parser.add_argument('-l', metavar='<lexicon>', required=True)
    parser.add_argument('-i', metavar='<invlists>', required=True)
    parser.add_argument('-m', metavar='<map>', required=True)
    parser.add_argument('-s', metavar='<stoplist>')
    parser.add_argument('query', metavar='<queryterm-1> [<queryterm-2> ... <queryterm-N>]', nargs='+')
    args = parser.parse_args()

    query_label = args.q
    num_results = int(args.n)

    start_time = time()

    map = {}
    lexicon = {}
    accumulators = {}

    with open(args.m, 'r') as map_file, open(args.l, 'r') as lexicon_file:
        for line in map_file:
            id, docno, weight = line.split()
            map[id] = (docno, float(weight))
        for line in lexicon_file:
            term, byte_offset = line.split()
            lexicon[term] = byte_offset

    N = len(map)  # number of documents in the collection
    ranker = BM25()  # BM25 instance with default constants
    with open(args.i, 'rb') as invlists_file:
        for term in args.query:  # one term at a time
            if term in lexicon:  # term needs to exist in lexicon
                term = term.lower()  # normalize term
                byte_offset = int(lexicon[term])  # address of term
                invlists_file.seek(byte_offset)  # move to address of term
                document_frequency = unpack('I', invlists_file.read(4))[0]  # frequency of term
                for _ in range(document_frequency):  # iterate inverted list of term
                    docno, weight = map[str(unpack('I', invlists_file.read(4))[0])]  # get the docno
                    within_document_frequency = unpack('I', invlists_file.read(4))[0]  # get the within doc freq
                    if docno not in accumulators:  # create an accumulator for docno
                        accumulators[docno] = 0
                    accumulators[docno] += ranker.score(N, document_frequency, within_document_frequency, weight)  # accumulate score

    heap = []
    i = 0
    for docno, score in accumulators.iteritems():  # iterate accumulators
        if i < num_results:  # add first <num_results> accumulators to heap
            heappush(heap, (score, docno))
            i += 1
        else:  # heap is full
            if heap[0][0] < score:  # root score is lower than new score
                heap[0] = (score, docno)  # replace the root with new score
                heapify(heap)  # heapify

    top = []
    for _ in range(num_results):
        top.append(heappop(heap))

    rank = 1
    for top_tuple in reversed(top):
        print("%s %s %d %.3f" % (query_label, top_tuple[1], rank, top_tuple[0]))
        rank += 1

    print("\nRunning time: %d ms" % ((time() - start_time) * 1000))

if __name__ == "__main__":
    main()
