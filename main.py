from ast import parse
from ctypes.wintypes import tagRECT
import json
import argparse
from api.api import start_api
import config.config_loading
from data import sql_reader
from data.data_aggregator import get_aggregate_dataframe
from data.preprocessing import data_organization
from machine_learning.classification import train_classifier
import pandas as pd
from data import sql_reader

args = argparse.ArgumentParser()
args.add_argument('--config', '-c', help="Loading the configuration for the entire system", required=True)
args.add_argument('--train', help="Activate the training for the machine learning model", required=False, action='store_true')
args.add_argument('--dataset', help="Get the dataset from file", type=str, required=False)
args.add_argument('--api', help="Activate the api", required=False, action="store_true")
parsed = args.parse_args()

configuration = config.config_loading.get_configuration(parsed.config)

#%% Connect to the database
db = sql_reader.connect_to_database(configuration['database']['host'], configuration['database']['user'], configuration['database']['passwd'], configuration['database']['name'], configuration['database']['port'])

#%% Create the base configuration
if parsed.train:
    print("Preparing model training...")
    if parsed.dataset is not None:
        dataframe = pd.read_csv(parsed.dataset)
    else:
        dataframe = get_aggregate_dataframe(db)
    print("Extract features")
    dataframe, target = data_organization.encode_target(configuration['save_path'], train_config=configuration['train'], dataframe=dataframe)
    dataframe, relation = data_organization.encode_relation(configuration['save_path'], dataframe=dataframe)
    
    train_classifier(configuration['train'], configuration['save_path'], data=dataframe)
    
elif parsed.api:
    if parsed.dataset is not None:
        start_api(config=configuration, db_connector=db, dataframe_path=parsed.dataset)
    else:
        start_api(config=configuration, db_connector=db)