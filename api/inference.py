import enum
from flask_restful import Resource
from flask import request
from machine_learning.multiclassification import infer_classifier
from data.training_data_reader import get_training_ids
import pandas as pd
import numpy as np
import os

configuration = {}
db_connector = None

def set_config(config):
    global configuration
    configuration = config
    
def set_db(db):
    global db_connector
    db_connector = db
    

#TODO adapt to the multiple models    

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
        # get the model_type from the query
        training_list = get_training_ids(db=db_connector)
        training_list = [str(i[0]) for i in training_list]
        if 'model' in data.keys():
            if data['model'] in ['occupation', 'skill']:
                model_type = data['model']
                keys = configuration['api']['inference'][model_type]['input_keys']
                if all(key in data['input'] for key in keys):
                    
                    # Opening the classification report:
                    report = pd.read_json(os.path.join(configuration['save_path']['report']['base_path'], configuration['model'][model_type]['name'].split('.')[0], configuration['save_path']['report']['classification']['textual']))
                    
                    dataframe = pd.DataFrame(data['input'], index=[0]) #TODO use the mapping for the relation_type in future development
                    inference, inference_prob, i_time = infer_classifier(save_config=configuration['save_path'], model_config=configuration['model'][model_type], input=dataframe)
                    inference_list = [name for index, name in enumerate(training_list) if inference[0][index] == 1.0]
                    inference_prob_list = [name for index, name in enumerate(inference_prob.tolist()[0]) if inference[0][index] == 1.0]
                    inference_dict = {}
                    for index, value in enumerate(inference_list):
                        inference_dict[int(value)] = inference_prob_list[index] 
                    
                    inference_dict = sorted(inference_dict.items(), key=lambda kv:(kv[1], kv[0]))
                    
                    response['status'] = 200
                    response['response']['result'] = inference_dict
                    response['response']['message'] = "Classification model executed"
                    response['response']['score'] = report.to_dict('records')[0]
                    response['response']['inference_time'] = i_time
                else:
                    response['status'] = 406
                    response['response']['message'] = "The input keys in the request does not respect what is expected from the ML algorithm"
            else:
                response['status'] = 406
                response['response']['message'] = "The specified model is not configured"
        else:
            response['status'] = 406
            response['response']['message'] = "You have to specify the model in the body of the request"
        return response
