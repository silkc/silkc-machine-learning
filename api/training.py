from flask_restful import Resource
from machine_learning.clustering import training_kmeans, save_model
from data.preprocessing.text_features_extraction import extract_features_from_text
import pandas as pd
ml_config = {}
dataset_path = ""

def set_config(config):
    global ml_config
    ml_config = config

def set_dataset_path(path):
    global dataset_path
    dataset_path = path

class Training(Resource):
    def get(self, source):
        response = {}
        if source in ['file', 'database']:
            if source == "file":
                dataframe = pd.read_csv(dataset_path)
            elif source == "database":
                dataframe = "null" #TODO change to SQL data
            features = extract_features_from_text(ml_config, dataframe,
                                                  ['occupation_preferred_label', 'occupation_description',
                                                   'isco_preferred_label', 'isco_group_description',
                                                   'occupation_skill_skill_type'], "english", True,
                                                  "hashing")

            km = training_kmeans(ml_config, features)
            save_model(ml_config, km)
        else:
            response = {"no"} #TODO change the response
        return {"ciao"}
