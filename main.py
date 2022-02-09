import json
import argparse
import config.config_loading
from data import sql_reader
from data.data_aggregator import get_aggregate_dataframe
import pandas as pd
from data.preprocessing.text_features_extraction import extract_features_from_text
from machine_learning.clustering import training_kmeans, save_model
from data import sql_reader
from api.api import start_api

args = argparse.ArgumentParser()
args.add_argument('--database_configuration', '-dbc', type=str, help="The path to the configuration of the database connection", required=False)
args.add_argument('--machine_learning_configuration', '-mlc', type=str, help="The path to the configuration of the machine learning")
args.add_argument('--train', help="Activate the training for the machine learning model", required=False, action='store_true')
args.add_argument('--dataset', help="Get the dataset from file", type=str, required=False)
args.add_argument('--api', help="Activate the api", required=False, action="store_true")
parsed = args.parse_args()

#%% get configuration
db_conf = config.config_loading.get_configuration(parsed.database_configuration)

#%% First step is dedicated to obtain all the data from the database
#%% create the dictionary that push all together.

#%% Connect to the database
db = sql_reader.connect_to_database(db_conf['db_host'], db_conf['db_user'], db_conf['db_passwd'], db_conf['db_name'], db_conf['db_port'])

#%% Opening Machine Learning configuration
with open(parsed.machine_learning_configuration, 'r') as config_file:
    ml_config = json.load(config_file)

#%% Create the base configuration
if parsed.train:
    print("Preparing model training...")
    if parsed.dataset is not None:
        dataframe = pd.read_csv(parsed.dataset)
    else:
        dataframe = get_aggregate_dataframe(db)
    print("Extracting features...")
    features = extract_features_from_text(
        ml_config,
        dataframe,
        [
            'training_id',
            'user_id',
            'user_occupation_id',
            'skill_id',
            'skill_occupation_id',
            'relation_type'
        ],
        "english",
        True,
        "hashing"
    )
    print("Training model...")
    km = training_kmeans(ml_config, features)
    print("Saving model...")
    save_model(ml_config, km)
    print("Training completed.")
elif parsed.api:
    if parsed.dataset is not None:
        start_api(ml_config=ml_config, db_connector=db, dataframe_path=parsed.dataset)
    else:
        start_api(ml_config=ml_config, db_connector=db)