# Main libraries 
from sklearn.linear_model import  LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import f1_score
from sklearn.svm import LinearSVC
from datetime import datetime
import numpy as np
import os

from features_extraction import *

########################### Start to train the model

def model_fit(model, X_train, y_train):
    """
    The function used to send sklearn model and fit the data on.
    Argument
        model   : model object, the model used to fitting data.
        X_train : array, 2-d array of training instances * features.
        y_train : array, 1-d array that represent the class associated with each instance.
    Return
        model   : model object, the model after fitting the data.
    """
    model.fit(X_train, y_train)
    return model

########################### End of train the model

########################### Start to validate the model

def f1_score_result(model, x, y):
    """
    The function used to test the model that we have trained.
    
    Argument
        model    : model object, the trained model.
        x        : array, 2-d array to test the model.
        y        : array, 1-d array that represent the class associated with each instance.
    Return
        micro_f1 : float, the score we got from validation.
    """

    predict                     = model.predict(x)
    micro_f1 = f1_score(y, predict, average='micro')

    print("===================== Validate Result =====================")
    print("F1 score is: ", micro_f1)

    return np.round(micro_f1, 3)

########################### End of validate the trained model

########################### Start to use Voting classifier

def voting_models():
    '''
    The function used to create three classifier for used multiple time.
    Argument
        No Argument
    Return
       estimators : list, The classifiers we create.
    '''

    svc_clf_model = LinearSVC(C=0.5,  max_iter=50, verbose=1)
    lg_clf_model  = LogisticRegression(penalty='l2', C=1, multi_class='multinomial', solver='lbfgs', verbose=1)
    dec_tree_clf_model  = DecisionTreeClassifier(max_depth=5, min_samples_split=2, min_samples_leaf=1)
    estimators = [("svc_clf_model", svc_clf_model), ("lg_clf_model", lg_clf_model), ("dec_tree_clf_model", dec_tree_clf_model)]
    return estimators

########################### End of use Voting classifier

########################### Start the pipeline of ml model

def ml_classifer_pipeline(model, X_train, y_train, X_val, y_val, used_word2vec_path, model_path_to_save):
    '''
    The function used to combine the pipeline of classification.

    Argument
        model              : model object, the model used to fitting data.
        X_train            : array, 2-d array of training instances * features.
        y_train            : array, 1-d array that represent the class associated with each instance.
        X_val              : array, 2-d array to test the model.
        X_val              : array, 1-d array that represent the class associated with each instance.
        used_word2vec_path : string, the path of related word2vec model we used.
        model_path_to_save : string, the path of the trained model to save in.
    Return
        model              : model object, the model after fitting the data.

    '''

    # To check how long time model take for training
    start                                       = datetime.now()

    # call model_fit function defined above
    model = model_fit(model, X_train, y_train)

    # call f1_score_result function defined above
    micro_f1 = f1_score_result(model, X_val, y_val)

    # Get the name of the model we have trained to save in a file with its name along side the score of its validation.
    model_name = type(model).__name__
    model_path_to_save = os.path.join(model_path_to_save, used_word2vec_path)
    model_path_to_save = model_path_to_save + model_name + "_" + "_f1_" + str(micro_f1) + "_ml.sav" 
    _ = pickle_save_mode(model, model_path_to_save)
    print ("It takes to run: ", datetime.now() - start)
    return model

########################### End of the pipeline of ml model



