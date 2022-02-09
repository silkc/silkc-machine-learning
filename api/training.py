from flask_restful import Resource
from data.data_aggregator import get_aggregate_dataframe
from data.preprocessing import data_organization
from machine_learning.classification import train_classifier
import pandas as pd

configuration = {}
dataset_path = ""
db_connector = None

def set_config(config):
    global configuration
    configuration = config

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
                dataframe = get_aggregate_dataframe(db_connector)
            
            dataframe, target = data_organization.encode_target(configuration['save_path'], train_config=configuration['train'], dataframe=dataframe)
            dataframe, relation = data_organization.encode_relation(configuration['save_path'], dataframe=dataframe)
            
            train_classifier(configuration['train'], configuration['save_path'], data=dataframe)
            
            response['status'] = 201 # model created corrected
            response['response']['message'] = f"The model was successfully created with the use of the {source}"
            response['response']['model_path'] = configuration['save_path']['model'] + configuration['save_path']['model_name']
            response['response']['mapping_paths'] = [
                configuration['save_path']['mapping']['target'] + configuration['save_path']['mapping']['target_name'],
                configuration['save_path']['mapping']['relation'] + configuration['save_path']['mapping']['relation_name']
            ]
            # TODO insert the metrics from test
        else:
            response['status'] = 404
            response['response']['message'] = "Model can be created because the source is not recognized"

        return response
