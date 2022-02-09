import pandas as pd
import numpy as np
import pickle
import os

def encode(dataframe: pd.DataFrame, column:str, save_mapping_path:str, use_saved:bool=False) -> pd.DataFrame:
    """[summary]

    Args:
        config ([type]): [description]
        dataframe (pd.DataFrame): [description]
    """
    targets = dataframe[column].unique()
    if use_saved:
        map_to_int = load_encoding(save_mapping_path)
    else:
        map_to_int = {name: n for n, name in enumerate(dataframe[column], start=1)}
        save_ecoding(save_path=save_mapping_path, encodered_dict=map_to_int)
    
    dataframe[column + "_int"] = dataframe[column].replace(map_to_int)
    return dataframe, targets

def encode_target(save_config:dict, train_config: dict, dataframe: pd.DataFrame):
    if os.path.exists(save_config['mapping']['target']):
        return encode(dataframe=dataframe, column=train_config['target_column'], use_saved=True, save_mapping_path=os.path.join(save_config['mapping']['target'], save_config['mapping']['target_name']))
    else:
        return encode(dataframe=dataframe, column=train_config['target_column'], save_mapping_path=os.path.join(save_config['mapping']['target'], save_config['mapping']['target_name']))

def encode_relation(save_config:dict, dataframe: pd.DataFrame):
    if os.path.exists(save_config['mapping']['relation']):
        return encode(dataframe=dataframe, column="relation_type", use_saved=True, save_mapping_path=os.path.join(save_config['mapping']['relation'], save_config['mapping']['relation_name']))
    else:
        return encode(dataframe=dataframe, column="relation_type", save_mapping_path=os.path.join(save_config['mapping']['relation'], save_config['mapping']['relation_name']))

def save_ecoding(save_path:str, encodered_dict:dict) -> None:
    
    save_file = open(save_path, "wb")
    pickle.dump(encodered_dict, save_file)
    save_file.close()
    
def load_encoding(save_path:str) -> dict:
    save_file = open(save_path, "rb")
    encodered_dict = pickle.load(save_file)
    save_file.close()
    return encodered_dict
