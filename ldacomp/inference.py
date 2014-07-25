# Bismillahi-r-Rahmani-r-Rahim
#
# Compute probabilities of documents


from gensim.models.ldamodel import LdaModel
from gensim.corpora import Dictionary

import settings


class InferenceModel(object):
    def __init__(self):
        self.model = LdaModel.load(settings.lda_model_name)
        self.dictionary = Dictionary.load_from_text(settings.wordids_txt)
        
    def prob(self, words):
        bow = self.dictionary.doc2bow(words)
        if len(bow) != len(words):
            print "One or more words missing from dictionary"
        return self.model.inference([bow])

