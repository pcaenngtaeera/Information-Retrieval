# Inverted Index

## About

Our project has programs: `index.py`, `search.py`. and `_vb` variations:

- `index.py` creates an inverted index for a given collection

- `search.py` outputs documents in the collection matching the search query
 
- `_vb` variations use variable-byte encoing to save disk space

## Index

Run `python index.py [-s stoplist] [-p] collection`:

- `[-s stoplist]` ignored words in the file when constructing the index
- `[-p]` prints each indexed word to `stdout`

On successful run, files `map`, `lexicon`, and `invlists` are created in the current working directory.

## Search

Run `python search.py lexicon invlists map [query...]`

- `[query...]` is a string of space separated terms

## References

The collection `latimes` is from [TREC](https://en.wikipedia.org/wiki/Text_Retrieval_Conference).

The stop words `stoplist` are from [Zettair](http://www.seg.rmit.edu.au/zettair/index.html).

The variable-byte encoding is based on the implementation in [Introduction to Information Retrieval](https://nlp.stanford.edu/IR-book/html/htmledition/variable-byte-codes-1.html).
