import os
import pandas as pd
import re
import emojis
from langdetect import detect_langs, detect
from googletrans import Translator
from datetime import datetime
DATA_DIR = "datasets/"
DATA_PREPROCESSED_DIR = "data_preprocessed/"

############## Regular Expression compiles to speed the process #############

# get urls in text 
URL_REPLACE        = re.compile(r"http\S+")

# get mentions in text
MENTIONED_REPLACE  = re.compile(r"@[A-Za-z0-9_]+")

# get more than one space between words
MORE_SPACES        = re.compile('([\s\t\n]+)')

# get chars repeated more than two times sequntially
CHAR_REPEATED      = re.compile('(.)\1+')

# remove dicrstics in text like(ً ُ)
TASHKEEL           = re.compile(r'[\u0617-\u061A\u064B-\u0652]')

# make a space between numbers asscoiated with words 
SEP_NUM_WORD       = re.compile('(\d+)')

# TRAN = Translator()
# SPACES_BET_2_CHAR  = re.compile('(!)[\s](!)')
# HASHTAG_REPLACE   = re.compile(r"#[A-Za-z0-9_]+")

########################## Helpful Functions ######################################

######################### start reading files

def read_file(file_path):
    '''
    The function used to read csv file.
    Argument
        file_path   : path, where is the path of the file to read
    Return 
        readed_data : the file we have readed
    '''
    readed_data = pd.read_csv(file_path)
    return readed_data

######################### End reading files

######################### start path handling function 
def save_filtered_tweets_path(year, data_preprocessed_dir=DATA_PREPROCESSED_DIR):
    '''
    The function used to save the filtered Arabic tweets,
    which will be used dierctly to extract numbers from.

    Argument
        data_preprocessed_dir : path, The direction we save the cleaned tweets in
    Return
        file_path             : File path to save the filted tweets in 
    '''
    dir_joined  = os.path.join(data_preprocessed_dir, "cleaned_arabic_tweets/") 
    file_name   = 'arabic_filtered_tweets_of_year_' + year + '.csv'
    file_path   = dir_joined + file_name
    return file_path

######################### End path handling function

######################################### Start Filter The Arabic tweets based on language column

def filter_1_get_arabic_data_based_on_language_column(data, language_col='language', language='ar'):
    '''
    The function used to get the Arabic data based on the language of tweets.

    Argument
        data         : data frame file, csv file
        language_col : string, Language columns in the readed file
        language     : string, Which language you need the tweets in (Arabic as it our interest)
    Return
        arabic_data: same csv file but with just Arabic tweets
    '''
    # Retrieve the data based on the language
    arabic_data = data[data[language_col] == language]

    # instead of 0, 1, 4, 8 because of get only Arabic rows, we reset to 0,1,2,3 and so on
    # Reset the index on same column in  in the csv file
    arabic_data.reset_index(inplace=True, drop=True)

    return arabic_data


def filter_2_get_only_arabic_tweets_column(year, data_dir=DATA_DIR, 
    data_preprocessed_dir=DATA_PREPROCESSED_DIR):
    '''
    The function used to get only the Arabic tweets from the csv files.

    Argument
        year                  : string, The year we need to get all Arabic tweets from all months we have collected before
        data_dir              : path, The main direction contain all of your data
        data_preprocessed_dir : path, The direction we save the cleaned tweets in
    Return
        all_arabic_tweeets    : list, that contain all the Arabic tweets of that year     
    '''
    # List to collect tweets in
    all_arabic_tweeets_in_year          = []

    # concat the main direction with the year we need in the loop like (data_dir + year)
    year_dir                            = os.path.join(data_dir, year)

    # For each month in that year 
    for month in os.listdir(year_dir):
        
        # Get all days files of some month of some year
        days_files                      = os.listdir(os.path.join(year_dir, month))

        # For each day in that month of this year
        for day in days_files:

            # Get full path of that file 
            file_path                   = os.path.join(year_dir, month, day)

            # Read the data in that file using read_file function defined
            readed_data                 = read_file(file_path)

            # Retrive the Arabic data from that file using filter_2_get_only_arabic_tweets_column function defined
            arabic_data                 = filter_1_get_arabic_data_based_on_language_column(readed_data, 
                                                    "language", "ar")

            # Just get only the tweets column as list
            arabic_tweets_in_day        = list(arabic_data['tweet'])

            # Append the tweets to our main list that collect all tweets of year
            all_arabic_tweeets_in_year += arabic_tweets_in_day
        break
    # After get all these tweets of that year save it in one file to use dierctly later
    print("="*50)
    # save the Arabic tweets we get from that year into new csv file of that year
    file_name                           = 'arabic_tweets_based_on_tweets_column_of_year_' + year + '.csv'
    file_path_to_save                   = data_preprocessed_dir + file_name

    # make a dataframe from the list of tweets as dictionary (key, value) to be saved as csv file
    tweets_data_frame                   = pd.DataFrame({'tweets': all_arabic_tweeets_in_year})
    tweets_data_frame.to_csv(file_path_to_save, index=False)
    return True


######################################### End Filter The Arabic tweets based on language column


####################### start cleaned and get filtered Arabic tweets using detect language of tweet

def text_to_clean(text):
    '''
    The function used to:
        - Clean / Normalize Arabic Text
        - Replace url with Non-standard Arabic name
        - Replace mentions with Non-standard Arabic name
        - Remove TASHKEEL (Special chars for Arabic language)
        - Remove char repeated more that two times sequentially
        - Separate numbers associated with words 
        - Multiple emojis coming sequentially leave just one of them
        - Remove more spaces
    Argument
        text: string, The text we need to handle
    Return
        text: string, the cleaned text after preprocessing it
    '''
    
    search  = ["أ","إ","آ","ة","_","-","/",".","،"," و "," يا ",'"',"ـ","'","ى","\\",'\n', '\t','&quot;','?','؟','!']
    replace = ["ا","ا","ا","ه"," "," ","","",""," و"," يا","","","","ي","",' ', ' ',' ',' ? ',' ؟ ',' ! ']
    
    # Replace the url with non-standard Arabic word 
    text = URL_REPLACE.sub("رابطويب", text)

    # Replace the mention with non-standard Arabic word 
    text = MENTIONED_REPLACE.sub("حسابشخصي", text)

    #remove tashkeel
    text = TASHKEEL.sub("", text)
    
    #remove longation (char repeated more that 2 times)
    text = CHAR_REPEATED.sub("\1\1", text)

    # Seprate numbers and words
    text = SEP_NUM_WORD.split(text)
    text = ' '.join(text)

    # some special replacement
    text = text.replace('وو', 'و')
    text = text.replace('يي', 'ي')
    text = text.replace('اا', 'ا')

    # lists defined in the begining of the function
    # search for these list of chars and replace it with value in same position 
    for i in range(0, len(search)):
        text = text.replace(search[i], replace[i])

    # decode emojis as text
    text = emojis.decode(text)
    
    # each emojis is decoded into :some text:
    text = re.split('(:\w+:)+', text)
    
    # convert text splited to list to string again and encode again the emojis text to emjois icon
    text = ''.join(text)
    text = emojis.encode(text)

    #remove more than one space between words
    text = MORE_SPACES.sub(" ", text)

    return text


def filter_3_save_cleaned_and_detected_arabic_tweets(all_arabic_tweeets_in_year, year, data_dir=DATA_DIR, 
    data_preprocessed_dir=DATA_PREPROCESSED_DIR, text_to_clean=text_to_clean):
    '''
    The function used to handle list of text using the text_to_clean function above, and other preprocess.
    
    Argument
        tweets                : list, of tweets we need to handle
        year                  : strin, in which year these tweets are
        data_dir              : path, the main dierction of the data
        data_preprocessed_dir : path, The direction we save the cleaned tweets in
        text_to_clean             : function, the function defined above to clean text

    '''
    
    cleaned_filtered_arabic_tweets = []

    print("The number of tweets in that year are: ")
    print(len(all_arabic_tweeets_in_year))

    # to check how long time preprocessing pipeline take
    start                                       = datetime.now()
    # loop over tweets in the list
    for i, tweet in enumerate(all_arabic_tweeets_in_year):

        # call the text_to_clean function to clean tweet
        tweet                                   = text_to_clean(tweet)
        
        # try to detect tweet language and save only Arabic tweets
        try:
            if detect(tweet) == 'ar':
                cleaned_filtered_arabic_tweets += [tweet]
        except:
            pass

        # save all tweets after each 100000 iteration to avoid missing all if there is crash
        if (i+1) % 100000    == 0:
            print("After Filtration part of tweets, number of Arabic tweets now are:")
            print(str(len(cleaned_filtered_arabic_tweets)) + " for year: " + year)

            # Save this Filtrated part of Arabic tweets in case of crash to start from this point
            file_path_to_save   = save_filtered_tweets_path(year, data_preprocessed_dir)
            
            tweets_data_frame = pd.DataFrame({'tweets': cleaned_filtered_arabic_tweets})
            tweets_data_frame.to_csv(file_path_to_save, index=False)
            print (datetime.now() - start)

    # Once we have end of all tweets save it again to get all cleaned tweets 
    print("After Filtration All tweets, number of Arabic tweets now are::")
    print(str(len(cleaned_filtered_arabic_tweets)) + " for year: " + year)

    # Save All Filtrated Arabic tweets of that year
    file_path_to_save   = save_filtered_tweets_path(year, data_preprocessed_dir)

    tweets_data_frame = pd.DataFrame({'tweets': cleaned_filtered_arabic_tweets})
    tweets_data_frame.to_csv(file_path_to_save, index=False)
    print("The overall time we took to preprocess all of our data is:")
    print (datetime.now() - start)
    return True


def filter_3_clean_get_arabic_tweets_by_detect_language(year, file_name="arabic_tweets_based_on_tweets_column_of_year_",
             data_dir=DATA_DIR,  data_preprocessed_dir=DATA_PREPROCESSED_DIR):
    '''
    The function used to get all Arabic tweets based on language detection after,
    we have saved from first filtered step based on language column.

    Argument
        year                  : string, The year we need to get all Arabic tweets from all months we have collected before
        file_name             : The name of the file we need to save filtered Arabic tweets in
        data_dir              : path, The main direction contain all of your data
        data_preprocessed_dir : path, The direction we save the filtered Arabic tweets in
    '''

    file_path_to_read          = data_preprocessed_dir + file_name + year + '.csv'
    readed_file                = pd.read_csv(file_path_to_read, lineterminator='\n')

    # Get all Arabic tweets in that year
    all_arabic_tweeets_in_year = list(readed_file['tweets'])
    # print(len(all_arabic_tweeets_in_year))
    _                          = filter_3_save_cleaned_and_detected_arabic_tweets(all_arabic_tweeets_in_year, year, 
                                        data_dir, data_preprocessed_dir, text_to_clean=text_to_clean)
    return True



####################### End cleaned and get filtered Arabic tweets using detect language of tweet
