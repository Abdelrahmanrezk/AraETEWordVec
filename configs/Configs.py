from sklearn.model_selection import StratifiedShuffleSplit
import os
import re
import pandas as pd
from nltk import ngrams
# from .DifferentTokenization import DifferentTokenization

# Related to send_exception method
current_dir = os.getcwd() 
parent_dir = os.path.dirname(current_dir)

# Directions used in functions
logs_dir = parent_dir + '/logs/'

stopwords_dir = parent_dir + '/hands_on_development/stop_words/'

tokenized_dir = parent_dir + '/hands_on_development/datasets/csv/step3_tokenization/'

vocabulary_dir = parent_dir + '/hands_on_development/datasets/csv/vocabulary/'

file_dir1                    =  stopwords_dir  + 'nltk_stop_words_handle.txt'
file_dir2                    =  stopwords_dir  + 'stop_list1.txt'
file_dir3                    =  stopwords_dir  + 'updated_stop_words.txt'



# Reading methods

def read_csv_file(file_path):
    '''
    The function used to read csv file.

    Argument:
    file_path: Which csv file you need to read.

    Return:
    cleaned_classifed_tweets_copy: Copy from the dataframe.
    '''
    cleaned_classifed_tweets_original = pd.read_csv(file_path)
    cleaned_classifed_tweets_copy = cleaned_classifed_tweets_original.copy()
    return cleaned_classifed_tweets_copy



# Tokenizers

def tokenization_stem_lemma_stop(tokenization_tokens,file_path, classes,
                    ar_stopwords, ar_stemming, ar_lemmtaization,
                    stop_words=True, stem=True, lemma=True, tokenizer_type="nltk_tokenizer"):
    
    '''
    The function used to handle different tokenization with different (stem, lemma and stopwords),
    we use two different tokenizer nltk and spacy tokenizer, also we need to experiment
    each of these tokenizer with (stem, lemma and stopwords) to use later in preparing stage,
    which help us run the model with different pre-process stages.
    
    Argument:
    tokenization_tokens : Which tokenizer you have got these tokens
    file_path           : the file path to save the tokenized list after pre-processing
    classes             : classes (label) associated with tweets
    ar_stopwords        : object from the stopwords class to remove stopwords from text
    ar_stemming         : object from the steamming class to collect different inflection of word under one word by remove prefix and suffix
    ar_lemmtaization    : object from the lemmtaization class to collect different inflection of word under one word using language rules
    stop_words          : As we have multiple experiments so is to work with stopwords in this experiment or not
    stem                : As we have multiple experiments so is to work with stemming in this experiment or not
    stop_words          : As we have multiple experiments so is to work with lemmtaization in this experiment or not
    tokenizer_type      : Which tokenization method you used to handle case of spacy token as string

    Return:
    df_preprocessed_text: The saved dataframe of tweets after pre-processing stage. 
    '''

    tokens = tokenization_tokens.copy() 
    if stem:
        tokens = ar_stemming.all_string_stemming(tokens, tokenizer_type)

    if stop_words:
        tokens = ar_stopwords.all_string_stop_words(tokens)

    if lemma:
        tokens = ar_lemmtaization.all_string_lemmatization(tokens, tokenizer_type)
    
    df_preprocessed_text = save_tokenized_lists(file_path, tokens, classes)
    list_of_words      = convert_list_of_lists_to_one_list(tokens, tokenizer_type)
    df_vocabulary_file = save_vocabulary(list_of_words, 'nltk_vocab_from_without_stem_and_without_stop.csv')
    print(df_vocabulary_file[:10])
    
    return df_preprocessed_text



# send files and save into directions

def send_exception(file_to_open, method_name, message, exception, LOGS_DIR=logs_dir):
	'''
	The method used to send errors occurred to logs direction and keep the errors away from the users.
	
    Argument:
	file_to_open: which file of errors you need to put the errors in.
	method_name: which method the error occured in.
	message: the error base message like it comes from specific file and specific class.
	exception: the error itself.
    LOGS_DIR(defined in the beginning of file):   The direction we send the error.
    
    Return
    True: once the exception sent
	'''

	file = open(LOGS_DIR+ file_to_open,"+a")
	file.write(message + "in method " + method_name + "\n" + 
	       "*** Error Type *** : " +str(exception) + "\n" + ("#" * 99) + "\n")
	file.close()
	return True

def save_tokenized_lists(file_path, text_list, classes, TOKENIZED_DIR=tokenized_dir):
    '''
    The function used to save the different tokenization with different preprocess stages:
    
    Argument:
    TOKENIZED_DIR(defined in the beginning of file): the dierction you need to save the work in,
    file_path    : the file path inside TOKENIZED_DIR with its name and its extention to save in that dierction,
    text_list    : list of lists each of these list are set of the words that consist the sentence,
    classes      : each of these list in test_list have the class which the classification of these words(sentence)
    
    Return:
    df_tokenized_file: dataframe of the same text_list but after we have save it along with classes
    '''

    dicts = {"tokenized_text":text_list , "class": classes}
    df_tokenized_file = pd.DataFrame(dicts)
    df_tokenized_file.to_csv(TOKENIZED_DIR + file_path, index=False)

    return df_tokenized_file

def save_vocabulary(list_of_words, file_path, VOCABULARY_DIR=vocabulary_dir):
    '''
    The function used to save the unique tokens from our corpse,
    these unique words we get after some of preprocess stage.
    
    Argument:
    list_of_words: All the tokens in our courps after some preprocess stage.
    file_path    : the file path inside TOKENIZED_DIR with its name and its extention to save in that dierction,
    VOCABULARY_DIR(defined in the beginning of file): the dierction you need to save the work in,

    Return:
    df_vocabulary_file: All the unique tokens from our corps.
    '''
    dicts = {"vocabulary":list_of_words}
    df_vocabulary_file = pd.DataFrame(dicts)
    df_vocabulary_file.to_csv(VOCABULARY_DIR + file_path, index=False)

    return df_vocabulary_file



# Conversion methods

def convert_list_of_lists_to_one_list(text_list, tokenizer_type="spacy_tokenizer"):
    '''
    The function used to convert list of lists which each of these list are set of the words
    in the sentence, so we convert to one list contain all words, 
    but after that get the unique words from this list.

    Argument:
    text_list      : list of lists each of these list are set of the words that consist the sentence,
    tokenizer_type : Which tokenization method you used to handle case of spacy token as string

    Return:
    list_of_words: The Vocabulary of our corps
    '''

    list_of_words = []
    if tokenizer_type == "spacy_tokenizer":
        if type(text_list[0][0]) != str:
            for indx, tokenized_sentence in enumerate(text_list):
                tokenized_sentence = [token.orth_ for token in tokenized_sentence]
                text_list[indx] = tokenized_sentence
    for lst in text_list:
        list_of_words += lst

    # Display result
    print("The number of Tokens are: ", len(list_of_words))

    list_of_words = sorted(set(list_of_words))
    print("#"*50)
    print("The number of Vocabulary are: ", len(list_of_words))

    return list_of_words

def convert_files_of_stop_words_to_list():
    '''
    The function used to get all the design files for stop words in one list.
    
    No Argument

    return:
    stop_words_designed: list of these stop words
    '''

    # The three direction in the beginning of file
    files = [file_dir1, file_dir2, file_dir3]
    stop_words_designed         = []
    for file_dir in files:
        with open(file_dir, 'r') as file:
            file                = file.readlines()
            file                = "".join(file)
            file                = re.sub('[\[\]\'\",]', '', file)
            stop_words_designed.extend(file.split())

    stop_words_designed         = list(set(stop_words_designed))
    return stop_words_designed



# Splitting Data
def splitting_train_dev_test(data, split_on):
    '''
    The function used to split data based on the target output, but not general shuffle,
    we use StratifiedShuffleSplit which help us to get approximate ratio of classes for each group.
    StratifiedShuffleSplit produce representative ratio of each class.
    
    Argument:
    data    : Dataframe contain tweets and predicted class of each tweet.
    split_on: How to split the data based on which feature so we use the class of the tweet, as it categorical feature.
    
    Return:
    strat_train_set_: Which our model will train on, to fitting the best as it can.
    strat_dev_set   : Which will evaluate your result of trained model on to fine-tune the hyperparameters.
    strat_test_set  : This part of data will be saved for later evaluation once we decide to launch our model to real life.
    
    '''
    
    # split into train and test then save the test data for time you decide to launch your model.
    split_train_test    = StratifiedShuffleSplit(n_splits=1, test_size=.05, random_state=42)
    for train_index, test_index in split_train_test.split(data, data[split_on]):
        strat_test_set  = data.loc[test_index]
        strat_train_set = data.loc[train_index]
        
        # Take part for validation
        strat_train_set       = strat_train_set.reset_index(drop=True)
        split_train_dev       = StratifiedShuffleSplit(n_splits=1, test_size=.05, random_state=42)
        for train_index_, dev_index in split_train_dev.split(strat_train_set, strat_train_set[split_on]):
            strat_train_set_  = strat_train_set.loc[train_index_]
            strat_dev_set     = strat_train_set.loc[dev_index]
    
    # Reset index for each dataframe
    strat_train_set_    = strat_train_set_.reset_index(drop=True)
    strat_test_set      = strat_test_set.reset_index(drop=True)
    strat_dev_set       = strat_dev_set.reset_index(drop=True)
    
    return strat_train_set_, strat_test_set, strat_dev_set








# Comparison methods
def compare_different_tokenizer(*argv):
    '''
    The function used to compare different tokenizer result.
    
    Argument:
    We can pass any number of argument as we have multiple tokenizer and we can add more.
    
    Return:
    True: once the loops end.
    '''
    for i in range(0, len(argv[0]), argv[-1]):
        print(len(argv[0][i]), len(argv[1][i]), len(argv[2][i]))

    return True

def get_ngrams(text_list, n=2):
    '''
    return the tweet u-gram and n-gram
    '''
    ng_text_list = []
    for tweet in text_list:
        ng_text_list += [tweet]
        ngs = [ng for ng in ngrams(tweet, n)]
        ng_text_list += [["_".join(ng) for ng in ngs if len(ng)>0 ]]
    return ng_text_list
