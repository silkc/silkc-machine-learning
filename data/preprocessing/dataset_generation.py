import pandas as pd
#from pprint import pprint

def adding_columns(model_config:dict, dataframe:pd.DataFrame, columns_name:list) -> pd.DataFrame:
    # Delete the NaN input
    dataframe.dropna(subset=model_config['input_columns'], how="any", inplace=True)
    # create the multi-labeled dataset
    dataframe_rows_number = len(dataframe.index)
    for name in columns_name:
        dataframe[name] = [0] * dataframe_rows_number
    for index, row in dataframe.iterrows():
        id = row[model_config['target_column']]
        dataframe.at[index, id] = 1
        #If the data is concatenated with commas, use the following instead
        #id_list = row[model_config['target_column']].split(',')
        #for id in id_list:
        #    dataframe.at[index, id] = 1
    return dataframe