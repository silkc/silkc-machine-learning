from sklearn.multiclass import OneVsRestClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import hamming_loss, zero_one_loss
import numpy as np
import pandas as pd
import pickle
import time
import os


def train_classifier(model_config:dict, save_config:dict, data:pd.DataFrame, target_column_name:list):
    
    classifier = OneVsRestClassifier(DecisionTreeClassifier(min_samples_split=model_config['train']['min_samples_split'], random_state=model_config['train']['random_state']))
    
    train, test = train_test_split(data, test_size=model_config['train']['split_percentage'])
    
    train_features = train[model_config['input_columns']]
    train_target = train[target_column_name]
    
    test_features = test[model_config['input_columns']]
    test_target = test[target_column_name]
    
    classifier.fit(train_features, train_target)
    
    save_model(save_config['model']['base_path'], model_config['name'], classifier)
    
    test_result = test_classifier(classifier, test_features, test_target)
    
    save_classification_report(report=test_result, save_path=os.path.join(save_config['report']['base_path'], model_config['name'].split('.')[0], save_config['report']['classification']['textual']))
    
    return classifier

def save_model(save_path, save_name, model):
    """

    :param config:
    :param model:
    :return:
    """
    import os
    os.makedirs(save_path, exist_ok=True)
    pickle.dump(model, open(os.path.join(save_path, save_name), 'wb'))
    return None

def load_model(save_path:str, model_name: str):
    """

    :param config:
    :return:
    """

    model = pickle.load(open(os.path.join(save_path, model_name), 'rb'))

    return model

def test_classifier(model, features, target):
    
    prediction = model.predict(features)
    
    accuracy = model.score(features, target)
    
    h_l = hamming_loss(target, prediction)
    z_o_l = zero_one_loss(target, prediction, normalize=False)
    z_o_l_n = zero_one_loss(target, prediction, normalize=True)
    
    score = {
        "hamming_loss": h_l,
        "zero_one_loss": z_o_l,
        "zero_one_loss_normalized": z_o_l_n,
        "accuracy": accuracy
    }
    
    return score

def save_classification_report(report:dict, save_path):
    
    df = pd.DataFrame(report, index=[0])
    
    df.to_json(save_path)

def infer_classifier(save_config, model_config, input):
    
    model = load_model(save_config['model']['base_path'], model_config['name'])
    
    start_time = time.time()
    
    prediction = model.predict(input)
    prediction_prob = model.predict_proba(input)
    
    end_time = time.time()
    
    inference_time = end_time - start_time
    
    return prediction, prediction_prob, inference_time