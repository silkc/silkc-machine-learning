from distutils.command.config import config
from urllib import response
from flask_restful import Resource
from flask import request
from machine_learning.classification import infer_classifier
import pandas as pd
import os

configuration = {}
db_connector = None

def set_config(config):
    global configuration
    configuration = config
    
def set_db(db):
    global db_connector
    db_connector = db
    
class Inference(Resource):
    
    def post(self):
        
        response = {
            "status": 0,
            "response": {
                "message": "",
                "result": 0,
                "accuracy": 0.0,
                "inference_time": 0
            }
        }
        
        data = request.get_json(force=True)
        keys = configuration['api']['inference']['input_key']
        if all(key in data['input'] for key in keys):
            # Opening the classification report:
            report = pd.read_json(os.path.join(configuration['save_path']['report']['base_path'], configuration['save_path']['report']['report_name']))
            
            dataframe = pd.DataFrame(data['input'], index=[0]) #TODO use the mapping for the relation_type
            inference, i_time = infer_classifier(config=configuration, input=dataframe)
            response['status'] = 200
            response['response']['result'] = int(inference[0])
            response['response']['message'] = "Classification model executed"
            response['response']['accuracy'] = report['precision']['accuracy']
            response['response']['inference_time'] = i_time
        else:
            response['status'] = 406
            response['response']['message'] = "The keys in the request does not respect what is expected from the ML algorithm"
        return response