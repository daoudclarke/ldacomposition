from ldacomp.restricted import RestrictedWikiCorpus
from ldacomp.dataset import Dataset

from gensim.corpora import HashDictionary
from gensim.corpora.wikicorpus import WikiCorpus

import settings

def test_restricted_wiki_has_terms_of_interest():
    dictionary = HashDictionary(id_range=100000)
    wiki = RestrictedWikiCorpus(settings.corpus, terms=['phone'],
                                dictionary=dictionary)
    page = next(wiki.get_texts())
    print page
    assert 'phone' in page


def test_get_interesting_proportion():
    dictionary = HashDictionary(id_range=100000)
    dataset = Dataset(settings.dataset)
    terms = dataset.all_lemmas()
    
    wiki = RestrictedWikiCorpus(settings.corpus, terms=terms,
                                dictionary=dictionary)
    
    num_pages = sum(1 for _ in wiki.get_texts())
    
    unrestricted = WikiCorpus(settings.corpus,
                              dictionary=dictionary)

    num_unrestricted_pages = sum(1 for _ in unrestricted.get_texts())
    print "Unrestricted: %d, restricted: %d" % (
        num_unrestricted_pages, num_pages)
