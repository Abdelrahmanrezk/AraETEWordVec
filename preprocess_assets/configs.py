import pandas as pd




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



def save_train_test_data(data, sub_dir, file_name_to_save, data_path=DATA_PATH):
    '''
    The function used to save the data after the spliting we apply to it.

    Argument
        data              : dataframe, the data you need to save.
        train_dir         : string, in which direction inside the main dataset direction you need to save your data.
        file_name_to_save : string, the csv file name you need to save the file with.
    '''
    # Get the full path to save the file

    file_path_to_save = data_path + sub_dir + file_name_to_save
    data.to_csv(file_path_to_save, index=False, encoding='utf8')

    return True