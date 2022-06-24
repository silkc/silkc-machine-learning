from flask_restful import Resource
from data.occupation.data_aggregator import get_aggregated_dataframe as o_aggregated
from data.skill.data_aggregator import get_aggregated_dataframe as s_aggregated
from data.total.data_aggregator import get_aggregated_dataframe as t_aggregated
from data.preprocessing import encoding, dataset_generation
from data.training_data_reader import get_training_ids
from machine_learning.multiclassification import train_classifier
from machine_learning.total_multiclassification import train_classifier as ttc
import pandas as pd
import os 

configuration = {}
datasets_path = ""
db_connector = None

def set_config(config):
    global configuration
    configuration = config

def set_datasets_path(path):
    global datasets_path
    datasets_path = path

def set_db(db):
    global db_connector
    db_connector = db


class Training(Resource):
    def get(self, model, source):
        response = {"status": 0,
                    "response":{}}
        if model in ['occupation', 'skill', 'total']:
            if source in ['file', 'database']:
                if model == 'occupation':
                    if source == 'file' and datasets_path is None:
                        response['status'] = 500 
                        response['response']['message'] = f"The file for the training has to be specified"
                        return response
                    elif source == 'file' and datasets_path is not None:
                        dataframe = pd.read_csv(os.path.join(datasets_path, 'occupation.csv'))
                    elif source == 'database':
                        dataframe = o_aggregated(db_connector)
                    training_list = get_training_ids(db=db_connector)
                    training_list = [str(i[0]) for i in training_list]
                    dataframe = dataset_generation.adding_columns(configuration['model']['occupation'], dataframe=dataframe, columns_name=training_list)
                    #dataframe, relation = data_organization.encode_relation(configuration['save_path'], dataframe=dataframe)
                    train_classifier(configuration['model']['occupation'], configuration['save_path'], data=dataframe, target_column_name=training_list)
                    
                    response['status'] = 201 # model created corrected
                    response['response']['message'] = f"The model was successfully created with the use of the {source}"
                    response['response']['model_path'] = configuration['save_path']['model']['base_path'] + configuration['model']['occupation']['name']
                    response['response']['mapping_paths'] = [
                        configuration['save_path']['mapping']['base_path'] + configuration['save_path']['mapping']['target'],
                        configuration['save_path']['mapping']['base_path'] + configuration['save_path']['mapping']['relation']
                    ]
                elif model == 'skill':
                    if source == 'file' and datasets_path is None:
                        response['status'] = 500 
                        response['response']['message'] = f"The file for the training has to be specified"
                        return response
                    elif source == 'file' and datasets_path is not None:
                        dataframe = pd.read_csv(os.path.join(datasets_path, 'skill.csv'))
                    elif source == 'database':
                        dataframe = s_aggregated(db_connector)
                    training_list = get_training_ids(db=db_connector)
                    training_list = [str(i[0]) for i in training_list]
                    dataframe = dataset_generation.adding_columns(configuration['model']['skill'], dataframe=dataframe, columns_name=training_list)
                    #dataframe, relation = data_organization.encode_relation(configuration['save_path'], dataframe=dataframe)
                    train_classifier(configuration['model']['skill'], configuration['save_path'], data=dataframe, target_column_name=training_list)
                
                    response['status'] = 201 # model created corrected
                    response['response']['message'] = f"The model was successfully created with the use of the {source}"
                    response['response']['model_path'] = configuration['save_path']['model']['base_path'] + configuration['model']['skill']['name']
                    response['response']['mapping_paths'] = [
                        configuration['save_path']['mapping']['base_path'] + configuration['save_path']['mapping']['target'],
                        configuration['save_path']['mapping']['base_path'] + configuration['save_path']['mapping']['relation']
                    ]
                elif model == 'total':
                    if source == 'database':
                        dataframe = t_aggregated(db_connector)
                    training_list = get_training_ids(db=db_connector)
                    training_list = [str(i[0]) for i in training_list]
                    dataframe = dataset_generation.total_adding_columns(dataframe=dataframe, target_column_name=configuration['model']['total']['target_column'], columns_name=training_list)
                    #dataframe, relation = data_organization.encode_relation(configuration['save_path'], dataframe=dataframe)
                    ttc(configuration['model']['total'], configuration['save_path'], data=dataframe, target_column_name=training_list)
                
                    response['status'] = 201 # model created corrected
                    response['response']['message'] = f"The model was successfully created with the use of the {source}"
                    response['response']['model_path'] = configuration['save_path']['model']['base_path'] + configuration['model']['skill']['name']
                    response['response']['mapping_paths'] = [
                        configuration['save_path']['mapping']['base_path'] + configuration['save_path']['mapping']['target'],
                        configuration['save_path']['mapping']['base_path'] + configuration['save_path']['mapping']['relation']
                    ]
            else:
                response['status'] = 404
                response['response']['message'] = "Model can be created because the source is not recognized"
        else:
            response['status'] = 404
            response['response']['message'] = "Model seletected does not exist"
        return response
