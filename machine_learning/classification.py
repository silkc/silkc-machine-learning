from sklearn.tree import DecisionTreeClassifier
import numpy as np
import pandas as pd
import pickle
import os

pd.set_option('mode.chained_assignment', None)

def train_classifier(model_config:dict, save_config:dict, data:pd.DataFrame):
    """[summary]

    Args:
        config ([type]): [description]
        data ([type]): [description]
    """
    classifier = DecisionTreeClassifier(min_samples_split=model_config['classificator']['min_samples_split'], random_state=model_config['classificator']['random_state'])
    
    data.dropna(subset=model_config['input_columns'], how="any", inplace=True)
    data.to_csv('./dataframe.csv')
    
    features = data[model_config['input_columns']]
    features.is_copy = False
    features.astype(np.float32)
    target = data[model_config['target_column']]
    
    classifier.fit(features, target)
    
    save_model(save_config, classifier)
    
    return classifier

def save_model(config, model):
    """

    :param config:
    :param model:
    :return:
    """
    import os
    save_path = os.path.join(config['model'], config['model_name'])
    os.makedirs(config['model'], exist_ok=True)
    pickle.dump(model, open(save_path, 'wb'))
    return None

def load_model(config):
    """

    :param config:
    :return:
    """

    model = pickle.load(open(os.path.join(config['save_path']['model'], config['save_path']['model_name']), 'rb'))

    return model

def infer_classifier(config, input):
    
    model = load_model(config=config)
    
    return model.predict(input)