# Main import libraries
from configs.Configs import send_exception
from nltk.tokenize import RegexpTokenizer, TreebankWordTokenizer
from spacy.lang.ar import Arabic
import nltk
import time
from datetime import datetime


#### ----------------------------Start DifferentTokenization Class------------------------------------ ####


class DifferentTokenization:
    """
    The class used to segment each document into words, for example:
    "Hello we are here" to be [Hello, we, are ,here]
    but using different library to compare the different tokenization library in time and accurate result.
    
    Inside each method we use different approach to compare in time.
    """
    
    
########################## Start Constructor

    def __init__(self, text_list, loops=True):
        '''
        Argument:
        text_list: which list of document each is a string you need to tokenize.
        loops: To compare using for loops and comprehensive for in time
        '''

        # To know from the error Raised in case of project go grow
        self.class_related_error       = "Raised error from test_Tokenization_timezation_of_cleaned_304418_classifed_tweets  file, class DifferentTokenization"
        try:                                                                                                                                                                
            # Handle the error 
            if not type(text_list) == list:
                raise Exception("TypeError -- You should pass a list of strings")
        except Exception as err:                                                                                                                                                                                                                                                                            
            send_exception("TypeError.log", "__init__", self.class_related_error, err)

        self.text_list                 = text_list
        self.loops                     = loops

        # instance private variable To get the tokenized documents related to the object it call.
        self.tokenized_text =          []                                                    

########################## End Constructor
    

########################## Start spacy Tokenizer
    
    def tokenize_using_spacy_library(self):
        '''
        The function used to segment document into tokens(words), 
        but based on spacy library, which have pre-defined rules for segmentation,
        and based on these rules of the language, it segment the document.
        
        Argument:
        self: Object reference
        
        No Return
        '''
        try:
            # Take and object from Arabic language
            arabic_nlp = Arabic()
            if self.loops:
                for text in self.text_list:
                    self.tokenized_text.append(list(arabic_nlp(text)))
            else:
                self.tokenized_text = [list(arabic_nlp(text)) for  text in self.text_list]

        # In case of error send to logs direction
        except:
            pass
            
########################## End spacy Tokenizer


########################## Start Regex Tokenizer

    def tokenize_using_nltk_RegexpTokenizer(self):
        '''
        The function used to segment document into tokens(words), 
        but based on nltk library, which have different approach, one of them is to define the tokenizer,
        based on regular expression you need and this one is RegexpTokenizer.
        
        Argument:
        self: Object reference
        
        No Return
        '''
        # Take and object from RegexpTokenizer tokenizer
        regs_tokenizer = RegexpTokenizer('\s+', gaps = True)
        i=0
        if self.loops:
            for text in self.text_list:
                try:
                    self.tokenized_text.append(regs_tokenizer.tokenize(text))
                    if (i+1) % 5000000 ==0:
                        print("We have tokenized: " + str(i+1))
                    i +=1
                except:
                    pass
        else:
            self.tokenized_text = [regs_tokenizer.tokenize(text) for  text in self.text_list]

########################## End Regex Tokenizer


########################## Start TreebankWord Tokenizer

    def tokenize_using_nltk_TreebankWordTokenizer(self):
        '''
        The function used to segment document into tokens(words), but based on nltk library, 
        but this time using TreebankWordTokenizer which more accurate, 
        and have its own pre-defined rules, and can know different between cases of points,
        in end of sentence and in decimal numbers as well as other rules.
        
        Argument:
        self: Object reference
        
        No Return
        '''

        # Take and object from TreebankWordTokenizer tokenizer
        tree_tokenizer = TreebankWordTokenizer()
        i=0
        if self.loops:
            for text in self.text_list:
                try:
                    self.tokenized_text.append(tree_tokenizer.tokenize(text))
                    if (i+1) % 5000000 ==0:
                        print("We have tokenized: " + str(i+1))
                    i +=1
                except:
                    pass
        else:
            self.tokenized_text = [tree_tokenizer.tokenize(text) for  text in self.text_list]



########################## End TreebankWord Tokenizer


########################## Start Retrive the Tokenized tweets

    def get_tokenized_text(self):
        """
        Just return tokenized_text as list of lists each list is contain its own tokens(words)
        
        Argument:
        self: Object reference
        
        No Return
        """
        return self.tokenized_text

########################## End Retrive the Tokenized tweets



#### ----------------------------End DifferentTokenization Class------------------------------------ ####


########################## start the use of Tokeinzer class based on different tokenizer ##########################


########################## Start Tokenization using Spacy

def test_spacy_Tokenization_time(text_list, loops=True):
    '''
    The function to test the spacy method of the class for how long time it take to documents in a list.
    
    Argument:
    text_list: list of strings to be processes
    loops: Is to use for loop or for comprehensive

    return:
    tokenizer: which can be used to access the tokenized documents
    '''

    copy_list = text_list.copy()
    start = datetime.now()
    tokenizer = DifferentTokenization(copy_list, loops)
    tokenizer.tokenize_using_spacy_library()
    end = datetime.now() - start

    # print("It takes about: ", str(end), "To process ", str(len(copy_list)), "Tweet")
    return tokenizer

########################## End Tokenization using Spacy


########################## Start Tokenization using Regex

def test_nltk_RegexpTokenizer_time(text_list, loops=True):
    '''
    The function to test the RegexpTokenizer method of the class,
    for how long time it take to documents in a list
    
    Argument:
    text_list: list of strings to be processes
    loops: Is to use for loop or for comprehensive 

    return:
    tokenizer: which can be used to access the tokenized documents
    '''
    copy_list = text_list.copy()
    start = datetime.now()
    tokenizer = DifferentTokenization(copy_list, loops)
    tokenizer.tokenize_using_nltk_RegexpTokenizer()
    end = datetime.now() - start

    # print("It takes about: ", str(end), "To process ", str(len(copy_list)), "Tweet")
    return tokenizer

########################## End Tokenization using Regex

########################## Start Tokenization using TreebankWord

def test_nltk_TreebankWordTokenizer_time(text_list, loops=True):
    '''
    The function to test the TreebankWordTokenizer method of the class,
    for how long time it take to documents in a list.
    
    Argument:
    text_list: list of strings to be processes
    loops: Is to use for loop or for comprehensive 

    return:
    tokenizer: which can be used to access the tokenized documents
    '''
    copy_list = text_list.copy()
    start = datetime.now()
    tokenizer = DifferentTokenization(copy_list, loops)
    tokenizer.tokenize_using_nltk_TreebankWordTokenizer()
    end = datetime.now() - start

    # print("It takes about: ", str(end), "To process ", str(len(copy_list)), "Tweet")
    return tokenizer

########################## End Tokenization using TreebankWord


#### ------------------------------------------------------------------------------------------------------- ####
