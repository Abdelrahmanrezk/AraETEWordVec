# Main import libraries
from gensim.models import Word2Vec
from datetime import datetime
from multiprocessing import cpu_count
from gensim.test.utils import get_tmpfile
from gensim.models.callbacks import CallbackAny2Vec
import multiprocessing
from ara_vec_preprocess_configs import *
############################## Need to document once thw work is compelted

manager = multiprocessing.Manager()
TOKENS_COUNT = manager.list()

class EpochSaver(CallbackAny2Vec):
    '''Callback to save model after each epoch.'''

    def __init__(self, path_prefix):
        self.path_prefix = path_prefix
        self.epoch = 0

    def on_epoch_end(self, model):
        output_path = self.path_prefix
        model.save(output_path)
        self.epoch += 1


class EpochLogger(CallbackAny2Vec):
    '''Callback to log information about training'''

    def __init__(self):
        self.epoch = 0

    def on_epoch_begin(self, model):
        print("Epoch #{} start".format(self.epoch))
        print (datetime.now())

    def on_epoch_end(self, model):
        print("Epoch #{} end".format(self.epoch))
        print (datetime.now())
        print("="*50)
        self.epoch += 1



class MyCorpus(object):
    def __init__(self, fname, gram_type):
        self.fpath          =  ARABIC_FILTERED_DATA_DIR + fname
        self.tree_tokenizer    = TreebankWordTokenizer()
        self.gram_type     = gram_type
        self.VAL = 0

    """An interator that yields sentences (lists of str)."""
    def __iter__(self):
        readed_data                 = read_file(self.fpath)
        tweets                      = list(readed_data['tweets'])
        del readed_data
        for tweet in tweets:
            try:
                unigram = self.tree_tokenizer.tokenize(tweet)
                gram_tokenized = unigram
                if self.gram_type == "fullgram":
                    gram_tokenized = get_all_ngrams([unigram], 3)

                self.VAL += len(gram_tokenized[0])
                yield gram_tokenized[0]
            except:
                pass

def train_word2vec_cbow(model, update, gram_type, sentences, vector_size=300, min_count=100):
    epoch_logger = EpochLogger()
    model_to_save  = "continuous_bow_" + gram_type + "_vec_size_" + str(vector_size) + "-d" +  "_min_count_" + str(min_count)
    epoch_saver = EpochSaver("models/Twittert-CBOW/CBOW_space_" + str(vector_size) + "/" + gram_type +  "/min_count_" + str(min_count) + "/" + model_to_save)
    start = datetime.now()

    if not update:
        print("="*50)
        print(update)
        model = Word2Vec(sentences=sentences, vector_size=vector_size, window=3, min_count=min_count, epochs=7,
         sample=1e-5,  workers=9, negative=0, sg=0, hs=1, callbacks=[epoch_logger, epoch_saver])

    elif update:
        print("="*50)
        print(update)
        model.build_vocab(sentences, update=update)
        model.train(sentences, total_examples=model.corpus_count, epochs=model.epochs, callbacks=[epoch_logger, epoch_saver])
    
    model.save("models/Twittert-CBOW/CBOW_space_" + str(vector_size) + "/" + gram_type +  "/min_count_" + str(min_count) + "/" + model_to_save)
    
    print (datetime.now() - start)

    return model

def train_word2vec_skip_gram(model, update, gram_type, sentences, vector_size=300, min_count=100):
    epoch_logger = EpochLogger()
    model_to_save  = "skip_gram_" + gram_type + "_vec_size_" + str(vector_size) + "-d" +  "_min_count_" + str(min_count)
    epoch_saver = EpochSaver("models/Twittert-Skip-Gram/Skip_Gram_space_" + str(vector_size) + "/" + gram_type +  "/min_count_" + str(min_count) + "/" + model_to_save)
    start = datetime.now()

    if not update:
        print("="*50)
        print(update)
        model = Word2Vec(sentences=sentences, vector_size=vector_size, window=3, min_count=min_count, epochs=7,
         sample=1e-5,  workers=9, negative=0, sg=1, hs=1, callbacks=[epoch_logger, epoch_saver])
    elif update:
        print("="*50)
        print(update)
        model.build_vocab(sentences, update=update)
        model.train(sentences, total_examples=model.corpus_count, epochs=model.epochs, callbacks=[epoch_logger, epoch_saver])
    
    model.save("models/Twittert-Skip-Gram/Skip_Gram_space_" + str(vector_size) + "/" + gram_type +  "/min_count_" + str(min_count) + "/" + model_to_save)
    
    print (datetime.now() - start)
    return model




def train_word2vec_skip_gram_negative_sampeling(model, update, gram_type, sentences, vector_size=300, min_count=100):
    epoch_logger = EpochLogger()
    model_to_save  = "sk_gr_negative_sampeling_" + gram_type + "_vec_size_" + str(vector_size) + "-d"  + "_min_count_" + str(min_count)
    epoch_saver = EpochSaver("models/Twittert-Skip-Gram-negative-sampeling/Skip_Gram_ns_space_" + str(vector_size) + "/" + gram_type +  "/min_count_" + str(min_count) + "/" + model_to_save)
    start = datetime.now()

    if not update:
        print("="*50)
        print(update)
        model = Word2Vec(sentences=sentences, vector_size=vector_size, window=3, min_count=min_count, epochs=7,
         sample=1e-5,  workers=9, negative=5, sg=1, hs=0, callbacks=[epoch_logger, epoch_saver])
    elif update:
        print("="*50)
        print(update)
        model.build_vocab(sentences, update=update)
        model.train(sentences, total_examples=model.corpus_count, epochs=model.epochs, callbacks=[epoch_logger, epoch_saver])
    
    model.save("models/Twittert-Skip-Gram-negative-sampeling/Skip_Gram_ns_space_" + str(vector_size) + "/" + gram_type +  "/min_count_" + str(min_count) + "/" + model_to_save)
    print (datetime.now() - start)
    return model



