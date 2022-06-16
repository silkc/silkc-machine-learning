import mysql.connector as mysql_connector
import pandas as pd

from data import sql_reader

def get_training_list(db: mysql_connector.CMySQLConnection, table:str = 'training', column_list:str = '*') -> list:
    return sql_reader.read_sql_data_to_list(db, table, column_list)

def get_training_dataframe(db: mysql_connector.CMySQLConnection, table:str = 'training', column_list:str = '*') -> pd.DataFrame:
    return sql_reader.read_sql_data_to_dataframe(db, table, column_list)

def get_training_ids(db: mysql_connector.CMySQLConnection, table:str = 'training', column: str = 'id') -> pd.DataFrame:
    return get_training_list(db, table, column_list=column)

if __name__ == "__main__":
    db = sql_reader.connect_to_database('localhost', 'root', 'root', 'SILCK', 33061)
    print(get_training_list(db))
    print(get_training_dataframe(db))