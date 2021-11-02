import argparse
import config.config_loading
from data import sql_reader

args = argparse.ArgumentParser()
args.add_argument('--database_configuration', '-dbc', type=str, help="The path to the configuration of the database connection")
args.add_argument('--machine_learning_configuration', '-mlc', type=str, help="The path to the configuration of the machine learning")
parsed = args.parse_args()

#%% get configuration
conf = config.config_loading.get_configuration(parsed.database_configuration)

#%% First step is dedicated to obtain all the data from the database
#%% create the dictionary that push all together.

#%% Connect to the database
db = sql_reader.connect_to_database(conf['db_host'], conf['db_user'], conf['db_passwd'], conf['db_name'])

#%%

