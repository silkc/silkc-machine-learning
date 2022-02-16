from ast import parse
from ctypes.wintypes import tagRECT
import os
import argparse
from api.api import start_api
import config.config_loading
from data import sql_reader
from data.occupation.data_aggregator import get_aggregated_dataframe as o_aggregated
from data.skill.data_aggregator import get_aggregated_dataframe as s_aggregated
from data.preprocessing import data_organization
from machine_learning.classification import train_classifier
import pandas as pd
from data import sql_reader

args = argparse.ArgumentParser()
args.add_argument('--config', '-c', help="Loading the configuration for the entire system", required=True)
args.add_argument('--train', help="Activate the training for the machine learning model, has to be in ['occupation', 'skill']", required=False, type=str)
args.add_argument('--datasets_path', help="Get the dataset from folder", type=str, required=False)
args.add_argument('--api', help="Activate the api", required=False, action="store_true")
parsed = args.parse_args()

configuration = config.config_loading.get_configuration(parsed.config)

#%% Connect to the database
db = sql_reader.connect_to_database(configuration['database']['host'], configuration['database']['user'], configuration['database']['passwd'], configuration['database']['name'], configuration['database']['port'])

#%% Create the base configuration
if parsed.train in ['occupation', 'skill']:
    if parsed.train == 'occupation':
        print("Preparing the OCCUPATION MODEL for the training")
        if parsed.datasets_path is not None:
            dataframe = pd.read_csv(os.path.join(parsed.datasets_path, 'occupation.csv'))
        else:
            dataframe = o_aggregated(db)
        dataframe, target = data_organization.encode_target(configuration['save_path'], train_config=configuration['model']['occupation'], dataframe=dataframe)
        #dataframe, relation = data_organization.encode_relation(configuration['save_path'], dataframe=dataframe)
        train_classifier(configuration['model']['occupation'], configuration['save_path'], data=dataframe)
    elif parsed.train == 'skill':
        print("Preparing the SKILL MODEL for the training")
        if parsed.datasets_path is not None:
            dataframe = pd.read_csv(os.path.join(parsed.datasets_path, 'skill.csv'))
        else:
            dataframe = s_aggregated(db)
        dataframe, target = data_organization.encode_target(configuration['save_path'], train_config=configuration['model']['skill'], dataframe=dataframe)
        #dataframe, relation = data_organization.encode_relation(configuration['save_path'], dataframe=dataframe)
        train_classifier(configuration['model']['skill'], configuration['save_path'], data=dataframe)
elif parsed.train not in ['occupation', 'skill'] and parsed.train is not None:
    raise(NotImplementedError(f"The {parsed.train} is not recognized as authorized parameter"))
if parsed.api:
    if parsed.datasets_path is not None:
        start_api(config=configuration, db_connector=db, dataframes_path=parsed.datasets_path)
    else:
        start_api(config=configuration, db_connector=db)