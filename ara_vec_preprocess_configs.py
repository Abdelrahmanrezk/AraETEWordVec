
# Main libraries 
from nltk.tokenize import RegexpTokenizer, TreebankWordTokenizer
from langdetect import detect_langs, detect
from datetime import datetime
from nltk import ngrams
import multiprocessing
import pandas as pd
import emojis
import os
import re



############## Start Main directions and global vairables #############

DATA_DIR = "datasets/"
DATA_PREPROCESSED_DIR = "data_preprocessed/"
ARABIC_FILTERED_DATA_DIR  = "cleaned_arabic_tweets/"


# Tweets Number from different stages
manager = multiprocessing.Manager()
NUM_SCRAP_TWEETS = manager.list()
NUM_AR_COL_TWEETS = manager.list()
NUM_RM_DUBLICATE_TWEETS = manager.list()
NUM_DETECT_AR_TWEETS = manager.list()

############## End Main directions and global vairables #############


############## Start heuristic design of Regular Expression compiles to speed the process #############

# get urls in text 
URL_REPLACE        = re.compile(r"http\S+")

# get mentions in text
MENTIONED_REPLACE  = re.compile(r"@[A-Za-z0-9_]+")

# get more than one space between words
MORE_SPACES        = re.compile(r'([\s\t\n]+)')

# get chars repeated more than two times sequntially
CHAR_REPEATED      = re.compile(r'(.)\1+')

# remove dicrstics in text like(ً ُ)
TASHKEEL           = re.compile(r'[\u0617-\u061A\u064B-\u0652]')

# make a space between numbers asscoiated with words 
SEP_NUM_WORD       = re.compile(r'(\d+)')

# make a space between English asscoiated with Arabic words 
SEP_EN_AR       = re.compile(r'[a-zA-Z]+')

# Uncide and emojis 
DETECT_SPECIAL_CHARS = re.compile("[\U0001f9bd\U0001f9d1\U0001f7e0\U000fe19b\U000fe19c\U000fe1b5\U000fe19d\U000fe19f\U000e0067\U0001f9b1\U000e007f\U000e0062\U000e006e\U000e0065\ue6fd\ue67b\ue67a\ue422\ue41f\ue327\ue224\ue40f\U000feb9d\ue703\U000fe527\ue677\ue222\ue221\uf8ff\ue694\U0001f7e1\U0001f90f\ue438\U000feb18\U0001f9dc\ue050\ue219\ue670\ue110\U0001f92e\U000feb5e\ue41d\ue32c\ue139\ue312\ue63e\ue748\U0001f7e2\ue046\ue033\ue112\U000fec17\ue335\ue035\ue44b\U000feb0d\U000fe32d\U000fe040\U0001f9e3\U000fe043\ue301\U0001fac2\ue009\U000fe354\ue00a\U000fe326\U000fe326\U000fe7f0\ue21d\ue21e\ue21f\ue444\ue66a\ue307\ue331\ue437\U0001f9a0\ue68d\ue405\ue21c\ue326\ue40c\ue03e\ue326\ue03e\U0001f9d6\ue304\U000fe987\ue681\U0001f993\ue305\ue427\ue303\ue118\ue404\ue32a\ue6ee\ue72d\ue6a4\ue22c\ue68d\U000fe1a8\ue20c\U0001fa84\ue04e\U000fe35b\U0001f9ed\U000fe54f\U000feb16\U000feb15\U000fe33d\ue704\ue105\ue01d\ue510\U000feb69\U000feb76\U000feb69\U000feb69\ue03f\ue12f\U000fe324\ue201\ue115\ue316\ue122\ue313\ue129\ue10f\ue03d\ue04a\ue02f\U000fe1b6\U000feb5c\ue058\ue71c\uf707\U000fe046\ue413\ue6e0\ue406\ue03c\ue042\ue411\ue410\U000fe333\U000fe041\ue402\ue6ec\ue72e\ue011\U000fe329\U000fe338\ue701\U000fe1b2\ue419\ue407\U000fe01f\U000feb75\U000feb85\ue022\U0001f9ba\ue347\ue32b\U000fe7d9\U000fe502\U0001f992\ue32e\U000feb5b\ue401\U000fe32a\U000fe1b3\U000fe341\U0001f9ce\ue314\ue725\ue32b\ue204\ue40e\ue00e\ue223\ue420\U0001f9d5\U0001f9e2\U0001fab0\U0001fac0\U0001f9e8\U0001f9d8\ue6ff\ue6fc\ue408\U0001f976\ue416\ue709\ue447\ue119\ue41b\U000fe351\ue418\ue148\U000fe335\ue030\ue31d\U0001fa78\ue747\ue702\ue306\ue106\ue698\ue057\ue529\U0001f91f\ue414\U000fe04d\U0001f9b9\U0001f90c\uf60d\U000fe532\ue67f\U000fe4f5\U0001f9e4\ue027\U000fe34a\ue409\ue22f\ue40a\ue049\ue04b\U000fe347\ue00f\U0001f9d4\ue754\ue311\ue113\U0001f964\ue11c\U000feb99\U000fec00\ue700\U0001f9e6\U000fe526\ue432\ue695\ue108\ue13c\ue319\ue676\U000fe03d\ue012\ue20f\ue220\U0001f972\ue6ac\U0001f966\ue643\u2060\U0001f9cd\U0001f9a7\U0001f962\ue328\ue71b\U000feb0f\U000feb6a\ue107\U000fe344\uf815\ue421\ue684\U0001f92f\U0001f9a6\U000fe358\ue6f6\ue008\U000feb9a\ue01b\U000fe340\ue70a\ue41e\U000feb55\ue056\ue32d\ue328\ue40d\ue337\ue743\ue417\ue023\ue403\ue6ef\ue6f0\ue415\ue056\ue022\ue412\U0001f92b\U000feb14\U0001f9b6\U000fe339\U000fe320\U000fe323\U000feb0e\U000fe342\U0001f92c\U000fe512\U000fe517\U000fe520\U000fe331\U000fe32c\U0001f971\U0001f9d0\U000fe33a\U0001f9ff\U0001f94d\U0001f975\U000fe19e\U000fe541\U000feb13\U0001f929\U000fe32f\U000fe343\U0001f9da\U0001f9af\ue757\U000fe1ab\U000fe1a5\U0001f928\U0001f9a5\U0001f974\U0001f973\U0001f90e\U0001f92a\U000feb9f\U000feb97\U000fe330\U000feb9e\U000fe334\U000feb96\ue537\U000fe327\U000fe334\U000fe33e\u200c\u200d\u202c\u200e\u202b\U0001f90d\u2067\u200f\u200b\U0001f97a\U0001f932\u2066\u2069\U0001f90d\U0001f970\U0001f92d\U0001f9e1\ue032\ue059\u06dd]")

# ############## End heuristic design of Regular Expression compiles to speed the process #############

#### ------------------------------------------------------------------------------------------------------- ####


# ########################## Start some Helpful Functions ######################################


########################## start reading files

def read_file(file_path):
    '''
    The function used to read csv file.
    Argument
        file_path   : path, where is the path of the file to read
    Return 
        readed_data : the file we have readed
    '''
    readed_data = pd.read_csv(file_path, lineterminator='\n')
    return readed_data

########################## End reading files


########################## Start reading all files than contain filtered Arabic tweets to tokenize it.

def tweets_to_build_word2vec_on(ar_filterd_dir=ARABIC_FILTERED_DATA_DIR):
    '''
    The function used to get all pre-processed Arabic tweets to tokenize for word2vec model.

    Argument:
        ar_filterd_dir : path, The direction we save the detected and cleaned tweets in
    '''

    # First get all the files in the direction
    years_files = os.listdir(ar_filterd_dir)

    # Make one list for all tweets of all years in files
    all_years_arabic_tweets = []

    for file in years_files:
        # Handle the path of the files we need to read
        file_path                   = ar_filterd_dir + file
        readed_data                 = read_file(file_path)
        tweets                      = list(readed_data['tweets'])

        # Append the tweets of the file to the main list 
        all_years_arabic_tweets    += tweets

    return all_years_arabic_tweets



########################## End reading all files than contain filtered Arabic tweets to tokenize it.


########################## Start expand the list to all tokens 

def convert_list_of_lists_to_one_list(text_list):
    '''
    The function used to convert list of lists which each of these list are set of the tokens
    in the tweet, so we convert to one list contain all tokens, which help us to know how many tokens in the data.

    Argument:
    text_list      : list, list of lists each of these list are set of the tokens that consist the tweets,

    Return:
    True
    '''

    list_of_all_tokens = []

    # Loop over each of these list of tokens, and append to one bigger list that contain all tokens
    for tokens in text_list:
        list_of_all_tokens += tokens

    # Display result
    print("="*50)
    print("The number of Tokens in our data are: ", len(list_of_all_tokens))
    print("="*50)
    print("first 50 tokens : ", list_of_all_tokens[:50])
    return True

########################## End expand the list to all tokens 


########################## Start get n-grams of tokens

def get_all_ngrams(tweets, nrange=3):
    '''
    The function used to get some n-grams instead of just uni-grams,
    like "We can do it" as uni-gram [We, can, do, it] it will be, [We_can, can_do, do_it] as bi-gram and so on.

    Arguemtn
        tweets: list, list that contain our tweets each of these tweets are list of tokens (uni-gram tokens)
    Return
        tweets: list, list that contain our tweets each of these tweets are list of tokens along with n-gram tokens
    '''

    for i, tweet in enumerate(tweets):
        ngs = []
        # get from uni-gram to n-grams you need for that tweet
        for n in range(1,nrange+1):
            ngs += [ng for ng in ngrams(tweet, n)]
            # seprate the grams by _ like We_can
            tweets[i] = ["_".join(ng) for ng in ngs if len(ng)>0 ]

        # As we have millions of tweets we need to check up the process
        if (i+1) % 5000000 == 0:
            print("Get ngrams of : " + str(i+1) + " Tweets")
    return tweets

########################## End get n-grams of tokens


########################## start path handling function 

def save_filtered_tweets_path(year, ar_filterd_dir=ARABIC_FILTERED_DATA_DIR):
    '''
    The function used to save the filtered Arabic tweets,
    which will be used dierctly to extract numbers from.

    Argument
        ar_filterd_dir        : string, The direction we need to save the detected Arabic tweets in.
    Return
        file_path             : string, File path to save the detected Arabic tweets in.
    '''

    file_name   = 'arabic_filtered_tweets_of_year_' + year + '.csv'
    file_path   = ar_filterd_dir + file_name
    return file_path

########################## End path handling function

########################### End some Helpful Functions ######################################

#### ------------------------------------------------------------------------------------------------------- ####

########################## Start first process Filteration the Arabic tweets ##########################

########################## Start filter to get the Arabic data based on the language of tweets.

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

########################## End  filter to get the Arabic data based on the language of tweets.

########################## Start to read all tweet files to Filter on language columns

def filter_2_get_only_arabic_tweets_column(year, data_dir=DATA_DIR, 
    data_preprocessed_dir=DATA_PREPROCESSED_DIR):
    '''
    The function used to get only the Arabic tweets from the csv files.

    Argument
        year                  : string, The year we need to get all Arabic tweets from all months we have collected before
        data_dir              : path, The main direction contain all of your data
        data_preprocessed_dir : path, The direction we save the tweets based in Arabic column.
    Return
        True, as we save our work on the disk     
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

            # Get how many tweets in that file before any preprocess step
            NUM_SCRAP_TWEETS.append(len(readed_data))


            # Call filter_2_get_only_arabic_tweets_column function to get only Arabic tweets based on language column
            arabic_data                 = filter_1_get_arabic_data_based_on_language_column(readed_data, 
                                                    "language", "ar")

            # Just get only the tweets column as list
            arabic_tweets_in_day        = list(arabic_data['tweet'])

            # Append the tweets to our main list that collect all tweets of one year
            all_arabic_tweeets_in_year += arabic_tweets_in_day
            break # do not forget to comment at the end
        break # do not forget to comment at the end

    # After get all these tweets of that year save it in one file to use dierctly later
    print("="*50)
    # save the Arabic tweets we get from that year into new csv file of that year
    file_name                           = 'arabic_tweets_based_on_tweets_column_of_year_' + year + '.csv'
    file_path_to_save                   = data_preprocessed_dir + file_name

    # make a dataframe from the list of tweets as dictionary (key, value) to be saved as csv file
    tweets_data_frame                   = pd.DataFrame({'tweets': all_arabic_tweeets_in_year})

    # Get how many tweets in after first filter of getting tweets based on the language columns
    NUM_AR_COL_TWEETS.append(len(tweets_data_frame))

    # Save our work into csv file
    tweets_data_frame.to_csv(file_path_to_save, index=False, encoding='utf8')

    return True

########################## End of read all tweet files to Filter on language columns


########################## End first process Filteration the Arabic tweets ##########################

#### ------------------------------------------------------------------------------------------------------- ####


########################## Start Second and last Filteration step ##########################

########################## Start to Clean / Normalize Arabic Tweets

def clean_str(text):
    '''
    The function used to Clean / Normalize Arabic Text:
        - Replace url with Non-standard Arabic name
        - Replace mentions with Non-standard Arabic name
        - Remove TASHKEEL (Special chars for Arabic language)
        - Remove part of appeared special chars like /U000f and others in DETECT_SPECIAL_CHARS defined in the begining
        - Some special replacement and handle the other replacement in the two list [search & replace]
        - Multiple emojis coming sequentially leave just one of them
        - Separate numbers associated with words as well as English with Arabic words
        - Remove char repeated more that two times sequentially
        - Remove more spaces
        
        
    Argument
        text: string, The text we need to handle
    Return
        text: string, the cleaned tweet after preprocessing it.
    '''
 
    search  = ['&quot;', "أ", "إ", "آ", "ة", "/", "!", '"', "'", "$", "%", "&", "(", ")", "*", "+", ",", "-", ".", ":", ";", "<", "=", ">", "?", "؟", "[", "]", "^", "_", "`", "{", "}", "|", "~", "ى","\\",'\n', '\t']
    replace = [' ', "ا", "ا", "ا", "ه", " / ", " ! ", "", "", " $ ", "%", " & ", " ( ", " ) ", " * ", " + ", " , ", "-", " . ", " : ", " ; ", " < ", " = ", " > ",  " ? ", " ؟ ", " [ ", " ] ", " ^ ", "_", " ` ", " { ", " } ", " | ", " ~ ", "ي"," \\ ",' ', ' ']
    
    # Replace the url with non-standard Arabic word 
    text = URL_REPLACE.sub(r"رابطويب", text)

    # Replace the mention with non-standard Arabic word 
    text = MENTIONED_REPLACE.sub(r"حسابشخصي", text)

    # remove tashkeel
    text = TASHKEEL.sub(r"", text)
    

    # By practice remove most appeared special chars like \U000f
    text = DETECT_SPECIAL_CHARS.sub('', text)
    
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
    
    #  each emojis is decoded into :some text:
    text = re.split(r"(:\w+:)+", text)
    
    #  convert text splited to list to string again and encode again the emojis text to emjois icon
    text = ' '.join(text)
    text = emojis.encode(text)

    # Seprate numbers and words
    text = SEP_NUM_WORD.split(text)
    text = ' '.join(text)

    # Seprate english and arabic
    text = SEP_EN_AR.sub(r' \g<0> ', text)

    # remove longation (char repeated more that 2 times)
    text = CHAR_REPEATED.sub(r"\1\1", text)

    # remove more than one space between words
    text = MORE_SPACES.sub(r" ", text)

    return text

########################## End of Clean / Normalize Arabic Tweets


########################## Start to detect and clean Arabic Tweets

def filter_3_save_cleaned_and_detected_arabic_tweets(all_arabic_tweeets_in_year, year, data_dir=DATA_DIR, 
    ar_filterd_dir=ARABIC_FILTERED_DATA_DIR, clean_str=clean_str):
    '''
    The function used to handle list of text using the clean_str function above, and other preprocess.
    
    Argument
        all_arabic_tweeets_in_year : list, of tweets we need to handle
        year                       : string, in which year these tweets are
        data_dir                   : string, the main dierction of the data
        ar_filterd_dir             : string, The direction we save the tweets based in Arabic column.
        clean_str                  : function, the function defined above to clean text
    
    Return
        True as we save our work on the disk    
    '''
    
    # list that will contain detected and cleaned Arabic tweets of each year.
    cleaned_filtered_arabic_tweets = []

    print("The number of tweets in that year are: ")
    print(len(all_arabic_tweeets_in_year))

    # to check how long time preprocessing pipeline take
    start                                       = datetime.now()
    # loop over tweets in the list
    for i, tweet in enumerate(all_arabic_tweeets_in_year):
    
        # try to detect tweet language and clean tweet if its Arabic
        try:
            # cleaned_filtered_arabic_tweets                                   += [clean_str(tweet)]
            # call the clean_str function to clean tweet
            if detect(tweet) == 'ar':
                tweet                                   = clean_str(tweet)
                cleaned_filtered_arabic_tweets += [tweet]
        except:
            pass

        # save all tweets after each 1000000 iteration to avoid missing all if there is crash
        if (i+1) % 1000000    == 0:
            print("After Filtration part of tweets, number of Arabic tweets now are:")
            print(str(len(cleaned_filtered_arabic_tweets)) + " for year: " + year)

            # Save this Filtrated part of Arabic tweets in case of crash to start from this point
            file_path_to_save   = save_filtered_tweets_path(year, ar_filterd_dir)
            
            tweets_data_frame = pd.DataFrame({'tweets': cleaned_filtered_arabic_tweets})

            tweets_data_frame.to_csv(file_path_to_save, index=False, encoding='utf8')
            print (datetime.now() - start)

    # Once we have end of all tweets save it again to get all cleaned tweets of some year
    print("After Filtration All tweets, number of Arabic tweets now are::")
    print(str(len(cleaned_filtered_arabic_tweets)) + " for year: " + year)

    # Save All Filtrated Arabic tweets of that year
    file_path_to_save   = save_filtered_tweets_path(year, ar_filterd_dir)

    tweets_data_frame = pd.DataFrame({'tweets': cleaned_filtered_arabic_tweets})
    
    # Shuffle data before saving
    tweets_data_frame                 = tweets_data_frame.sample(frac=1).reset_index(drop=True)

    # Save the data after all preprocess is done
    tweets_data_frame.to_csv(file_path_to_save, index=False, encoding='utf8')

    # Append how many tweets are now after detect and clean the Arabic tweets
    NUM_DETECT_AR_TWEETS.append(len(tweets_data_frame))

    print("The overall time we took to preprocess all of our data is:")
    print (datetime.now() - start)
    return True

########################## End of detect and clean Arabic Tweets


########################## Start the main filteration step and remove dublicated tweets in the files

def filter_3_clean_get_arabic_tweets_by_detect_language(year, file_name="arabic_tweets_based_on_tweets_column_of_year_",
             data_dir=DATA_DIR,  ar_filterd_dir=ARABIC_FILTERED_DATA_DIR, data_preprocessed_dir=DATA_PREPROCESSED_DIR):
    '''
    The function used to get all Arabic tweets based on language detection after,
    we have saved from first filtered step based on language column.

    Argument
        year                  : string, The year we need to get all Arabic tweets from all months we have collected before
        file_name             : string, The name of the file we need to save filtered Arabic tweets in
        data_dir              : string, The main direction contain all of your data
        data_preprocessed_dir : string, The direction we save the tweets based in Arabic column.

    Return
        True as we save our work on the disk    
    '''

    # Reading the csv files that contain the tweets from first filtration stage, which is language column
    file_path_to_read          = data_preprocessed_dir + file_name + year + '.csv'
    readed_file                = pd.read_csv(file_path_to_read, lineterminator='\n')

    # Drop repeated tweets
    readed_file                = readed_file.drop_duplicates(subset=['tweets'])

    # Append how many tweets after remove the dublicated tweets
    NUM_RM_DUBLICATE_TWEETS.append(len(readed_file))

    # Get all Arabic tweets in that year as python list
    all_arabic_tweeets_in_year = list(readed_file['tweets'])


    # Detect either it's Arabic tweet or not and clean the tweet if its Arabic tweet
    _                          = filter_3_save_cleaned_and_detected_arabic_tweets(all_arabic_tweeets_in_year, year, 
                                        data_dir, ar_filterd_dir, clean_str=clean_str)
    return True

########################## End the main filteration step and remove dublicated tweets in the files



########################## End of Second and last Filteration step ##########################


#### ------------------------------------------------------------------------------------------------------- ####
