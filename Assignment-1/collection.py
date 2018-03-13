import re
from collections import Counter


alphanumeric_pattern = re.compile('[\W_]+')
no_tags_pattern = re.compile('<(.*?)>')


class Document:
    def __init__(self, id, docno, terms):
        self.id = id
        self.docno = docno
        self.terms = terms


class Collection:
    def __init__(self):
        self.stoplist = []
        self.documents = []

    def get_documents(self, sourcefile):
        """
        Uses invariants of <sourcefile> to efficient parse the file:
            - <DOC> is the first line of <sourcefile>
            - </DOC> is the last line of <sourcefile>
            - Each </DOC> is followed by a </DOC> on the next line (excluding the final </DOC>)

        Splits the sourcefile into a list of document strings using the invariants.
        Increments an <id> to uniquely identify each document for mapping.
        """
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
        """
        Splits a given string into a list of terms while using regex to remove tags (e.g. <TAG></TAG>)

        Iterate the list of terms and cleans it up by:
            - regex to remove non-alphanumeric characters
            - case-fold into lower-case

        By splitting the string into a list of terms we handle token normalisation by:
            - removing hyphens for terms e.g. 0-312-02432-0 -> 0312024320
            - removing apostrophes for terms e.g. MARTIN'S -> martins

        Returns a list of terms that is filtered by the <stoplist> if it exists.
        """
        terms = []
        for term in no_tags_pattern.sub('', text).split():
            terms.append(alphanumeric_pattern.sub('', term).lower())
        if self.stoplist:
            return [t for t in terms if t not in self.stoplist]
        else:
            return terms

    def parse_document(self, id, text):
        """
        Uses invariants of <DOC></DOC> to efficiently parse documents:
            - <DOCNO></DOCNO> is the first line of the document
            - <HEADLINE> && </HEADLINE> appear individually on separate lines
            - <TEXT></TEXT> appear individually on separate lines

        Given a string with the contents of the document, stores each line in a list of lines.
        Determines position of the relevant tags and uses slicing to obtain relevant data.
        Passes data into extract_terms() function which returns a list of terms.

        Returns a list of terms in order of appearance
        """
        lines = text.split('\n')
        docno = lines[0][8:-9]
        n, s, e = 0, 0, 0
        markers = []
        for line in lines:
            if line == '<HEADLINE>' or line == '<TEXT>':
                s = n
            elif line == '</HEADLINE>' or line == '</TEXT>':
                e = n
                markers.append((s, e))
            n += 1
        terms = []
        for marker in markers:
            terms += lines[marker[0]:marker[1]]
        terms = self.get_terms(' '.join(terms))
        return Document(id, docno, terms)

    def use_stoplist(self, path):
        """
        TODO: Comments
        """
        with open(path, 'r') as f:
            self.stoplist = f.read().split('\n')

    def map_to_disk(self):
        """
        Writes a map of the <id> and <docno> of each document into the file <map> in the CWD.

        Each line represents a document using the format:
            - <id> + whitespace + <docno>

        If a file named <map> already exists, it is overwritten.
        """
        if self.documents:
            with open('map', 'w+') as f:
                for document in self.documents:
                    f.write(str(document.id) + ' ' + document.docno + '\n')

    def generate_inverted_index(self):

        """
        TODO: Stub
        """
        postings = {}
        if self.documents:
            for document in self.documents:
                for term in document.terms:
                    if postings.has_key(term):
                        postings[term].append(document.id)
                    else:
                        postings[term] = [document.id]

        offset = 0
        with open('invlists', 'w+') as i, open('lexicon', 'w+') as l:
            for term in postings.keys():
                counter = Counter(postings[term])
                l.write(term + ' ' + str(offset) + '\n')
                i.write(str(len(counter.keys())))
                for id in counter:
                    i.write(' ' + str(id) + ' ' + str(counter[id]))
                i.write('\n')
                offset += 1

    def print_terms(self):
        """
        TODO: Comments
        """
        if self.documents:
            for document in self.documents:
                for term in document.terms:
                    print(term)
