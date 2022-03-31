
# Main libraries 
from calendar import monthrange
import twint
import os


########################### Start some Helpful Functions ######################################

########################## start to check file availability

def check_file_exist_or_not(year, month, save_file_name):
    '''
    The function used to check if some files we have created before, and append the data into the same file.
    This help use append to same file with the same date and time.
    
    Argument
        year           : string, the year we are scrapped now.
        month          : string, which month of that year you looking for. 
        save_file_name : string, the csv file name to check it's available or not.

    Return 
        boolean
    '''
    # Get all files of that month in the year
    files = os.listdir('datasets/' + year  + "/Month_" + month + '/')

    for file in files:
        # Check file availability
        if file == save_file_name:
            return True
    return False

########################## End of check file availability

########################### End some Helpful Functions ######################################


#### ------------------------------------------------------------------------------------------------------- ####


########################### Start Scrapping ######################################


########################## Start to scrap tweets in some hour of some day

def tweets_for_one_hour(year, month, day, date_str):
    '''
    The function used to scrap tweets from twitter using twint project withing some day of some month and year.

    Argument
        year           : string, the year we are scrapped now.
        month          : string, which month of that year you looking for. 
        day            : string, Which day in that month you run the scrap.
        date_str       : string, At which time of that day you need to start the scrapper.

    Return 
        boolean
    '''

    # Initialize the class instance variables in Config file of twint project
    c = twint.Config()

    # Start the search for tweets 
    c.TwitterSearch = True

    # From which time in that day you need to start the scrap
    c.Until = date_str

    # How many returned tweets you need to scrap then stop the scrapping once it reach that limit
    c.Limit = 5000

    # For each tweet get these metadata, like tweet id at twitter, which user who write that tweet and so on
    c.Custom['tweet'] = ["id", "created_at", "username",  "tweet", "language", "hashtags", "geo"]

    # Because we should provide a search query not just the language of tweet
    # I provided the query with Arabic chars as I need any tweet in Arabic language
    c.Lang = 'ar'
    c.Search = 'أ OR إ OR ه OR ل OR ح OR م OR ق OR و OR ش OR ر OR ب OR ت OR س OR ك OR ن OR خ OR ص OR س OR ف OR ع OR ض OR ج OR د OR غ OR  ط OR ز OR ذ OR  ي OR ث OR ظ'
    
    # hide the tweets from be displayed as default
    c.Hide_output=True

    # Get the output into csv file
    c.Store_csv = True

    # Rename the csv file based on the tweets created at which time
    save_file_name = "with_data_time_" + date_str + "_" + ".csv"

    # Check if we get tweets into same file before, so do not created again, append to it
    if not check_file_exist_or_not(year, month, save_file_name):
        c.Output = 'datasets/' + year  + "/Month_" + month + '/' + save_file_name

    # Start the search for Arabic tweets
    try:
        twint.run.Search(c)
    except:
        pass

    return True

########################## End of scrap tweets in some hour of some day


########################## Start to scrap tweets in some day

def tweets_for_one_day(year, month, day):
    """
    The function used scrap tweets within some day of some month.

    Argument
        year           : string, the year we are scrapped now.
        month          : string, which month of that year you looking for. 
        day            : string, Which day in that month you run the scrap.

    Return 
        boolean
    """

    # Handle days like 1 to be 01
    if len(day) == 1:
        day = '0' + day

    # Handle monthes like 1 to be 01
    if len(month) == 1:
        month = '0' + month
    
    # Enhanced the scrapper to get tweets within same day from multiple hours    
    for i in range(23, 0, -5):
        # In which year-month-day-hour-minute-second you need to start your scrapper
        if i < 10: # To handle hours
            date_str = year + '-' + month + '-' + day + ' 0' + str(i) + ':40:00'
        else:
            date_str = year + '-' + month + '-' + day + ' ' + str(i) + ':40:00'

        # Start the scraping by calling the main function of scrap as described above
        _ = tweets_for_one_hour(year, month, day, date_str)

    return True

########################## End of scrap tweets in some day


########################## Start to scrap tweets in some month

def tweets_for_one_month(year, month):
    '''
    The function used scrap tweets within some month of some year.
    Argument
        year           : string, the year we are scrapped now.
        month          : string, which month of that year you looking for. 

    Return 
        boolean
    '''

    # Get the number of days in that month of this year based on calender in that year
    num_days = monthrange(year, month)[1]
    
    # Handle month as string
    month = str(month)

    # Handle monthes like 1 to be 01
    if len(month) == 1:
        month = '0' + month

    # In case dierction is not exist, create one with that month in that year
    try:
        os.mkdir('datasets/' + str(year) + '/Month_' + month)
    except:
        pass

    # for that month loop over its days
    for day in range(1, num_days +1):
        # Start to looking for tweets within that day of the month
        _ = tweets_for_one_day(str(year), month, str(day))
        print("Year: " + str(year) + " Month: " + month + " Day: " + str(day))
    return True

########################## End of scrap tweets in some month

def tweets_for_one_year(year):
    '''
    The function used scrap tweets within some year.
    Argument
        year           : string, the year we are scrapped now.

    Return 
        boolean
    '''
    # loop of months of each year
    for month in range(1, 13):
        _= tweets_for_one_month(year, month)
    
    return True


########################### End Scrapping ######################################