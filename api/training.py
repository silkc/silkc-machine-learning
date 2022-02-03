from flask_restful import Resource
from machine_learning.clustering import training_kmeans, save_model
from data.preprocessing.text_features_extraction import extract_features_from_text
from data.data_aggragator import get_aggregated_dataframe
import pandas as pd
ml_config = {}
dataset_path = ""
db_connector = None

def set_config(config):
    global ml_config
    ml_config = config

def set_dataset_path(path):
    global dataset_path
    dataset_path = path

def set_db(db):
    global db_connector
    db_connector = db


class Training(Resource):
    def get(self, source):
        response = {"status": 0,
                    "response":{}}
        if source in ['file', 'database']:
            if source == "file":
                dataframe = pd.read_csv(dataset_path)
            elif source == "database":
                dataframe = get_aggregated_dataframe(db_connector)
            features = extract_features_from_text(ml_config, dataframe,
                                                  ['occupation_preferred_label', 'occupation_description',
                                                   'isco_preferred_label', 'isco_group_description',
                                                   'occupation_skill_skill_type'], "english", True,
                                                  "hashing")

            km = training_kmeans(ml_config, features)
            save_model(ml_config, km)
            response['status'] = 201
            response['response']['message'] = "The model was successfully created"
            response['response']['model_path'] = ml_config['api_configuration']['model_path']
            response['response']['extractor_path'] = ml_config['api_configuration']['extractor_path']
        else:
            response['status'] = 404
            response['response']['message'] = "Model can be created because the source is not recognized"

        return response
