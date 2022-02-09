from distutils.command.config import config
from urllib import response
from flask_restful import Resource
from flask import request
from machine_learning.classification import infer_classifier
import pandas as pd

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
                "classification": 0,
                "accuracy": 0,
                "inference_time": 0
            }
        }
        
        data = request.get_json(force=True)
        dataframe = pd.DataFrame(data['input'], index=[0])
        inference = infer_classifier(config=configuration, input=dataframe)
        response['status'] = 200
        response['response']['classification'] = int(inference[0])
        return response