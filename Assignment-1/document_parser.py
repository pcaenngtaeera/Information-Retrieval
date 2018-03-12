import os
import re

class document():
    def __init__(self, id, docno, terms):
        self.id = id
        self.docno = docno
        self.terms = terms

class document_parser():
    def __init__(self, sourcefile):
        self.sourcefile = sourcefile
        self.documents = []
        self.stoplist = []

    def extract_terms(self, text):
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
        for term in re.sub(r'<(.*?)>', '', text).split():
            terms.append(re.sub(r'[\W_]+', '', term).lower())
        if self.stoplist:
            return [t for t in terms if t not in self.stoplist] 
        else:
            return terms

    def parse_document(self, id, text):
        """
        Uses invariants of <DOC></DOC> to efficiently parse documents:
            - <DOCNO></DOCNO> is the first line of the document
            - <HEADLINE> && </HEADLINE> appear individually on separate lines
            - <TEXT></TEXT> appear individually on separate lines after <HEADLINE> && </HEADLINE>

        Given a string with the contents of the document, stores each line in a list of lines.
        Determines position of the relevant tags and uses slicing to obtain relevant data.
        Passes data into extract_terms() function which returns a list of terms.

        Returns a list of terms in order of appearance
        """
        lines = text.split('\n')
        docno = lines[0][8:-9]
        n = 1
        for line in lines[1:]:
            if line == '<HEADLINE>':
                headline_start = n
            elif line == '</HEADLINE>':
                headline_end = n
            elif line == '<TEXT>':
                text_start = n
            elif line == '</TEXT>':
                text_end = n
            n += 1
        headline_terms = self.extract_terms(' '.join(lines[headline_start:headline_end]))
        text_terms = self.extract_terms(' '.join(lines[text_start:text_end]))
        return document(id, docno, headline_terms + text_terms)

    def extract_documents(self):
        """
        Uses invariants of <sourcefile> to efficient parse the file:
            - <DOC> is the first line of <sourcefile>
            - </DOC> is the last line of <sourcefile>
            - Each </DOC> is followed by a </DOC> on the next line (excluding the final </DOC>)

        Splits the sourcefile into a list of document strings using the invariants.
        Increments an <id> to uniquely identify each document for mapping.
        """
        if self.sourcefile:
            document_texts = self.sourcefile[6:-7].split("</DOC>\n<DOC>")
            id = 0
            for text in document_texts:
                self.documents.append(self.parse_document(id, text))
                id += 1

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
            f.close()

    def apply_stoplist(self, path):
        """
        TODO: Comments
        """
        with open(path, 'r') as f:
            self.stoplist = f.read().split('\n')

    def print_terms(self):
        """
        TODO: Comments [inorder print of terms]
        """
        if self.documents:
            for document in self.documents:
                for term in document.terms:
                    print(term)
