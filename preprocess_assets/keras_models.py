import time
import os
from keras.layers.embeddings import Embedding
from keras.models import Sequential
from keras.layers import Flatten
from tensorflow import keras
import time
import keras
import numpy as np
from sklearn.metrics import f1_score


TENSOR_DIR = os.path.join(os.curdir, "models", "dl_models", 'tensor_logs/')
MODELS_DIR = os.path.join(os.curdir, "models", "dl_models/") 


def get_run_tensor_logdir(run_hyper_params, tensor_dir=TENSOR_DIR):
    '''
    The function used to create dierction with the time we have run the model in, beside of that,
    concat to this time which hyperparameters we have used in this run, this time along with hyperparameters, 
    will help us compare result from different run with different hyperparamters, 
    as we used the tensorboard server as our vislization tool to help decide which model we can use.
    
    Argument:
        run_hyper_params: which hyper params we have used for this run.
        TENSOR_DIR: the tensor logs direction to be our direction for different runs.
        
    return
        tensor_dir + run id(which run along with hyperparams to create subdirectory for)
    '''
    
    run_id = time.strftime("run_%Y_%m_%d_%H_%M_%S_") + run_hyper_params
    return os.path.join(tensor_dir, run_id)





def lstm_no_batch_seqential_model_create(hid_num_neurons, max_len=64, number_of_features=100, dropout=.2):
    '''
    The function used to create keras Long short-term memory Sequential model.

    Argument
        hid_num_neurons    : int, the number of neurons to use with LSTM layer.
        max_len            : int, the maximum number of tokens we tend to use for each text.
        number_of_features : int, the number of flatten features of each token.
        dropout            : float, to avoid the overfitting.
    '''
    model = keras.models.Sequential()
    model.add(keras.layers.LSTM(hid_num_neurons, return_sequences=True, input_shape=(max_len, number_of_features)))
    model.add(keras.layers.Dropout(dropout))
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(18, activation="softmax"))
    return model



def lstm_with_batch_model_create(hid_num_neurons, max_len=64, number_of_features=100, dropout=.2):
    '''
    The function used to create keras Long short-term memory Sequential model with Batching Normalization.

    Argument
        hid_num_neurons    : int, the number of neurons to use with LSTM layer.
        max_len            : int, the maximum number of tokens we tend to use for each text.
        number_of_features : int, the number of flatten features of each token.
        dropout            : float, to avoid the overfitting.
    '''
    model = keras.models.Sequential()
    model.add(keras.layers.Input(shape=(max_len, number_of_features)))
    model.add(keras.layers.BatchNormalization())
    model.add(keras.layers.LSTM(hid_num_neurons, return_sequences=True, input_shape=(max_len, number_of_features)))
    model.add(keras.layers.BatchNormalization())
    model.add(keras.layers.Dropout(dropout))
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(18, activation="softmax"))
    return model

def seqential_model_compile(model, optimizer):
    '''
    The function used to compile keras model with Sequential API, and specific optimizer.

    Argument
        model     : The keras model create.
        optimizer : The optimizer of learning algorithm.
    '''
    model.compile(loss="sparse_categorical_crossentropy", optimizer=optimizer,
                  metrics=['accuracy'])
    return model


def keras_f1_score_result(model, x, y):
    """
    The function used to test the model that we have trained.
    
    Argument
        model    : model object, the trained model.
        x        : array, 2-d array to test the model.
        y        : array, 1-d array that represent the class associated with each instance.
    Return
        micro_f1 : float, the score we got from validation.
    """
    predict=model.predict(x) 
    predict=np.argmax(predict,axis=1)
    micro_f1 = f1_score(y, predict, average='micro')

    print("===================== Validate Result =====================")
    print("F1 score is: ", micro_f1)

    return np.round(micro_f1, 3)


def keras_callbacks(word2vec_type, model_type, learning_rate):
    '''
    The function used to save the models at end of each epoch, along with tensorboard to compare models.
    '''
     # Handle the different runs for the model to easily monitor from tensor board
    hyper_params = word2vec_type + "_" + model_type + "_learning_rate=" + str(learning_rate) + "_"
    run_log_dir = get_run_tensor_logdir(hyper_params, TENSOR_DIR)

    cb_tensor_board = keras.callbacks.TensorBoard(run_log_dir)

    # Once there is no progress stop the model and retrive the best weights
    cb_early_stop   = keras.callbacks.EarlyStopping(patience=5,monitor="val_loss",
                                                    restore_best_weights=True)

    # Handle problems that happend and long time training and save model check points
    file_path      = "/run_with_" + hyper_params +  "_model.h5"
    model_save_dir = MODELS_DIR + file_path
    cb_check_point = keras.callbacks.ModelCheckpoint(model_save_dir, monitor="binary_accuracy")

    # create list of callbacks we create
    callbacks = [cb_early_stop, cb_check_point, cb_tensor_board]

    return callbacks