from gensim.corpora.wikicorpus import WikiCorpus, _extract_pages, process_article, ARTICLE_MIN_WORDS
from gensim import utils

from itertools import imap
import bz2
import multiprocessing
import logging

logger = logging.getLogger(__name__)

class RestrictedWikiCorpus(WikiCorpus):
    def __init__(self, fname, terms, **args):
        self.terms = set(terms)
        super(RestrictedWikiCorpus, self).__init__(fname, **args)

    def get_texts(self):
        """
        Iterate over the dump, returning text version of each article as a list
        of tokens.

        Only articles of sufficient length are returned (short articles & redirects
        etc are ignored).

        Note that this iterates over the **texts**; if you want vectors, just use
        the standard corpus interface instead of this function::

        >>> for vec in wiki_corpus:
        >>>     print(vec)
        """
        articles, articles_all = 0, 0
        positions, positions_all = 0, 0
        texts = ((text, self.lemmatize, title, pageid) for title, text, pageid in _extract_pages(bz2.BZ2File(self.fname), self.filter_namespaces))
        #pool = multiprocessing.Pool(self.processes)
        # process the corpus in smaller chunks of docs, because multiprocessing.Pool
        # is dumb and would load the entire input into RAM at once...
        for group in utils.chunkize(texts, chunksize=10 * self.processes, maxsize=1):
            #for tokens, title, pageid in pool.imap(process_article, group): # chunksize=10):
            for tokens, title, pageid in imap(process_article, group): # chunksize=10):
                articles_all += 1
                positions_all += len(tokens)
                # Check if the article is long enough and has tokens in our set of interestx
                if len(tokens) > ARTICLE_MIN_WORDS and set(tokens) & self.terms:
                    articles += 1
                    positions += len(tokens)
                    if self.metadata:
                        yield (tokens, (pageid, title))
                    else:
                        yield tokens
        #pool.terminate()
        
        logger.info("finished iterating over Wikipedia corpus of %i documents with %i positions"
            " (total %i articles, %i positions before pruning articles shorter than %i words)" %
            (articles, positions, articles_all, positions_all, ARTICLE_MIN_WORDS))
        self.length = articles # cache corpus length
