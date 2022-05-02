from sklearn.model_selection import StratifiedShuffleSplit, train_test_split
import pandas as pd
from collections import Counter
# from configs import *



########################### Start random splitting

def general_split_and_shuffle(data, split_percentage=.02):
    '''
    The function used to split the data using random split. 

    Argument
        data             : dataframe, the data you need to split into training and test.
        split_percentage : float, The percentage of split you need to apply for training and testing.
    Return
        train_set        : dataframe, the splited trainig set.
        test_set         : dataframe, the splited testing set.
    '''

    # First general shuffle , frac it determines what fraction of total instances need to be returned.
    data                = data.sample(frac=1).reset_index(drop=True)

    # random splitting
    train_set, test_set = train_test_split(data, test_size=split_percentage)

    print("The number of instances in the training data after train_test_split are: ", len(train_set))
    print("The number of instances in the testing data after train_test_split are:  ", len(test_set))


    return train_set, test_set

########################### End of random splitting

########################### Start Stratified splitting

def Stratified_split_and_shuffle(data, dialect_col_to_split_on, split_percentage=.02):
    '''
    The function used to distribute the splitting across different classes and ensure that, 
    we have representative number of instance per total number of instance for each class,
    not just that it helps to make approximate distribution like what we have in orginal data.

    Argument
        data                    : dataframe, the data you need to split into training and test.
        dialect_col_to_split_on : string, Which categorical column you need your split to be based on.
        split_percentage        : float, The percentage of split you need to apply for training and testing.
    Return
        strat_train_set         : dataframe, the splited trainig set.
        strat_test_set          : dataframe, the splited testing set.
    '''

    # First general shuffle , frac it determines what fraction of total instances need to be returned.
    data                = data.sample(frac=1).reset_index(drop=True)

    # Get object from StratifiedShuffleSplit class, .02 as we have 458,197 instance so take about 10,000 for testing
    split               = StratifiedShuffleSplit(n_splits=1, test_size=split_percentage)


    for train_indices, test_indices in split.split(data, data[dialect_col_to_split_on]):
        strat_train_set = data.loc[train_indices] # retrive rows with these indices
        strat_test_set  = data.loc[test_indices] # retrive rows with these indices

    # Reset the indeces to be from 0
    strat_train_set     = strat_train_set.reset_index(drop=True)
    strat_test_set      = strat_test_set.reset_index(drop=True)

    print("The number of instances in the training data after StratifiedShuffleSplit are: ", len(strat_train_set))
    print("The number of instances in the testing data after StratifiedShuffleSplit are:  ", len(strat_test_set))

    return strat_train_set, strat_test_set

########################### End of Stratified splitting

########################### Start to get how many instances for each class

def dialect_proportions(data):
    '''
    The function used to get percentage of how many instances(samples) of each class we have.
    Argument
        data                   : dataframe, the data you need to check the counts of each class in some column.
    Return
        prop_sampels_per_class : array, proportions of each class counts
    '''
    prop_sampels_per_class = data["dialect"].value_counts() / len(data)
    return prop_sampels_per_class

########################### End of get how many instances for each class


########################### Start to get how many instances for each class

########################### Start to compare the two shuffling method we use

def compare_random_and_stratified_split(dialect_dataset, test_set, strat_test_set):
    '''
    The function used to compare how its random and stratified split are from spliting our data, 
    the second one ensure that we have proportions of each class instances related to what in the orginal data.
    Argument
        dialect_dataset  : dataframe, the orginal data to compare with.
        test_set         : dataframe, the test data created by random split.
        strat_test_set   : dataframe, the test data created by random stratified split.
    Return 
        comp_prop        : dataframe, the table that explain how different splitting are. 
    '''
    
    # Get percentage of the number of instances per class for each dataset
    overall                              = dialect_proportions(dialect_dataset)
    random_test                          = dialect_proportions(test_set)
    stratified_test                      = dialect_proportions(strat_test_set)
    comp_prop_dict                       = { 'Overall': overall,  'stratified_test': stratified_test,   'random_test':random_test }
    comp_prop                            = pd.DataFrame(comp_prop_dict)
    
    # First get how many instance of each class we got by * 100, then divide by the overall of instances of each class 
    comp_prop['stratified_test. %error'] = 100 * comp_prop["stratified_test"] / comp_prop["Overall"] - 100
    comp_prop['random_test. %error']     = 100 * comp_prop["random_test"] / comp_prop["Overall"] - 100

    return comp_prop


########################### End of compare the two shuffling method we use



def get_keys_that_val_gr_than_num(num_of_words_in_each_text, num):
    '''
    The function used to get dictionary that value of its keys are greater than some number.

    Argument
        num_of_words_in_each_text : list, The list to get the values repeated in as keys and how many times its repeated as value.
        num                       : int, Which keys its value grater than that num to save in your dictionary.
    Return
        new_dicts                 : dictionary, keys and its related repeated value greater than some num
    '''
    # get number of times the text has same number of tokens
    dicts = dict(Counter(num_of_words_in_each_text))

    # Get new object instead of reference to same dictionary as we do not need to delete of what we loop over.
    new_dicts = dicts.copy()

    print("The number of keys before removing are: ", len(new_dicts))
    print("="*50)
    for key, val in dicts.items():
        if val <= num:
            new_dicts.pop(key)

    print("The number of keys after removing some of them are: ", len(new_dicts))
    print("="*50)
    new_dicts = {key: val for key, val in sorted(new_dicts.items(), key=lambda item: item[1])}
    return new_dicts
    


########################### End of validate the data used and the new created data with new text column



def save_train_test_data(data, sub_dir, file_name_to_save):
    '''
    The function used to save the data after the spliting we apply to it.

    Argument
        data              : dataframe, the data you need to save.
        train_dir         : string, in which direction inside the main dataset direction you need to save your data.
        file_name_to_save : string, the csv file name you need to save the file with.
    '''
    # Get the full path to save the file

    file_path_to_save = sub_dir + file_name_to_save
    data.to_csv(file_path_to_save, index=False, encoding='utf8')

    return True