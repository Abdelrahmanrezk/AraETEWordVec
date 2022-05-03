# Main libraries 
from keras.preprocessing.sequence import pad_sequences
from gensim.models import Word2Vec
import pickle
from tensorflow import keras 

# Our files
# from configs import *
from data_shuffling_split import *





def load_word2vec_model(model_path):
    """
    The function used to load the word2vec model that we will use to get token representation from.
    
    Argument
        model_path        : string, the path where the models is saved.
    Return
        word_to_vec_model : model object, the word2vec trained model.
    """

    word_to_vec_model = Word2Vec.load(model_path)
    return word_to_vec_model

def pickle_save_mode(model,file_path):
    '''
    The function used to save sklearn models using pickle.

    Argument
        model     : model object, the model we need to save.
        file_path : string, the path where we need to save the models in with its name.
    Return
        True      : boolean, as there no error while we saved the model.
    '''

    pickle.dump(model, open(file_path, 'wb'))

    return True

def pickle_load_model(file_path):
    '''
    The function used to load sklearn models using pickle.

    Argument
        file_path : string, the path where the models is saved.
    Return
        model     : model object, the corresponding model we load.
    '''

    model = pickle.load(open(file_path, "rb"))
    return model

def keras_load_model(file_path):
    '''
    The function used to load sklearn models using pickle.

    Argument
        file_path : string, the path where the models is saved.
    Return
        model     : model object, the corresponding model we load.
    '''
    model = keras.models.load_model(file_path)
    return model




def prepare_data(data, ):
    '''
    The function used to prepare the data we will use as features(text),
    and the corresponding class associated with that text.
    
    Argument
        data         : dataframe, the data you need to split into training and validation.

    Return
        x_train_text : list, the training data we need to train our model on, but need to prepared as numbers.
        x_val_text   : list, the Validation data we need to validate the model trained on, but need to prepared as numbers.
        y_train      : array, the corresponding label for each text.
        y_val        : array, the corresponding label for each text.
    '''

    # Get the splited training and validation datasets. 
    # functionfrom Stratified_split_and_shuffle function defined in data_shuffling_split file
    x_train, x_val = Stratified_split_and_shuffle(data, "label", split_percentage=.02)

    # Separate text into lists
    x_train_text, x_val_text = list(x_train['text']), list(x_val['text'])

    # Separate labels into arrays as .values return numpy array
    y_train, y_val = x_train['label'].values, x_val['label'].values

    # Display some info after splitting
    print("The number of trainin instances: ", len(x_train_text))
    print("The number of validation instances: ",len(x_val_text))
    print("The number of trainin labels : ", len(y_train))
    print("The number of validation labels : ", len(y_val))

    return x_train_text, x_val_text, y_train, y_val



def text_to_matrix_using_word2vec(word_to_vec_model, text_list, max_len_str):
    """
    The function used to convert the preprocessed text into numbers using word2vec trained model.

    Argument
        word_to_vec_model : model object, the word2vec trained model.
        text_list         : list, list of list each of these list is tokenized string.
        max_len_str       : int, as we need to pass fixed length of each document we have to set to some fixed number.
    Return
        embedding_matrix  : array, 2-d matrix that hold the corresponding text list.
    """

    # Create list that we will use to append each sample after getting the representation of each of its tokens.
    embedding_matrix = []

    # llop over each list of tokens
    for text in text_list:
        # To get the corresponding tokens representation in.
        sampel_vec = []
        # For each token in that text get its representation.
        for token in text:
            try:
                sampel_vec.append(word_to_vec_model.wv[token])
            except KeyError:
                pass
        embedding_matrix.append(sampel_vec)

    # As we have different text with different number of tokens, so we need to map each of these different length,
    # into fixed length to train your models as it expect specific length (dimensions).
    # pad_sequences is a keras object that help us done this work.
    embedding_matrix = pad_sequences(embedding_matrix, maxlen=max_len_str, padding='post',  dtype='float16')

    print("="*50)
    print(embedding_matrix.shape)
    # This is for machine learning models but we will need to reshape it for deep learning models.
    embedding_matrix = embedding_matrix.reshape(embedding_matrix.shape[0], embedding_matrix.shape[1]*embedding_matrix.shape[2])
    
    print(embedding_matrix.shape)
    print("="*50)
    print(embedding_matrix[0][:50])
    return embedding_matrix


