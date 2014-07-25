# Bismillahi-r-Rahmani-r-Rahim

# Compute the LDA model from wikipedia dump

import logging, gensim, bz2

import settings

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def compute_lda_model(wordids_txt, tfidf_mm, output_name):
    id2word = gensim.corpora.Dictionary.load_from_text(wordids_txt)
    
    # load corpus iterator
    mm = gensim.corpora.MmCorpus(bz2.BZ2File(tfidf_mm))    

    # Run LDA
    lda = gensim.models.ldamodel.LdaModel(corpus=mm, id2word=id2word, num_topics=100, update_every=1, chunksize=10000, passes=1)
    lda.save(output_name)
    
    lda.print_topics(20)


if __name__ == "__main__":
    compute_lda_model(settings.wordids_txt,
                      settings.tfidf_mm,
                      settings.lda_model_name)
