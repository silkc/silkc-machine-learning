from tracemalloc import start
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import pickle
import time
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
    
    train, test = train_test_split(data, test_size=0.2)
    
    train_features = train[model_config['input_columns']]
    train_features.is_copy = False
    train_features.astype(np.float32)
    train_target = train[model_config['target_column']]
    
    test_features = test[model_config['input_columns']]
    test_target = test[model_config['target_column']]
    
    classifier.fit(train_features, train_target)
    
    save_model(save_config, classifier)
    
    prediction, report = test_classifier(classifier, test_features, test_target)
    
    os.makedirs(save_config['report']['base_path'], exist_ok=True)
    
    classification_report_csv(report=report, save_path=os.path.join(save_config['report']['base_path'], save_config['report']['report_name']))
    #confusion_matrix_plot(test_target, prediction, os.path.join(save_config['report']['base_path'], save_config['report']['cf_name']))
    
    return classifier

def classification_report_csv(report, save_path):
    df = pd.DataFrame(report).transpose()
    
    df.to_json(save_path)
    
def classification_overall(report, save_path):
    #THIS FUNCTION IS NOT USED AND NOT IMPLEMENT IT IS ONLY FOR FUTURE
    return None
    

def test_classifier(model, features, target):
    predicted = model.predict(features)
    
    report = classification_report(target, predicted, output_dict=True)
    
    return predicted, report

def confusion_matrix_plot(target, predicted, save_path):
    #Generate the confusion matrix
    cf_matrix = confusion_matrix(target, predicted)
    
    ax = sns.heatmap(cf_matrix, annot=True, cmap='Blues')

    ax.set_title('Seaborn Confusion Matrix with labels\n\n')
    ax.set_xlabel('\nPredicted Values')
    ax.set_ylabel('Actual Values ')

    ## Ticket labels - List must be in alphabetical order
    ax.xaxis.set_ticklabels(['False','True'])
    ax.yaxis.set_ticklabels(['False','True'])

    ## Display the visualization of the Confusion Matrix.
    #plt.show()
    plt.savefig(save_path)

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
    
    start_time = time.time()
    
    prediction = model.predict(input)
    
    end_time = time.time()
    
    inference_time = end_time - start_time
    
    return prediction, inference_time