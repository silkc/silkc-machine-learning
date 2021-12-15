import mysql.connector as mysql_connector
import pandas as pd

import sql_reader

def get_skill_list(db: mysql_connector.CMySQLConnection, table:str = 'skill', column_list:str = '*') -> list:
    return sql_reader.read_sql_data_to_list(db, table, column_list)

def get_skill_dataframe(db: mysql_connector.CMySQLConnection, table:str = 'skill', column_list:str = '*') -> pd.DataFrame:
    return sql_reader.read_sql_data_to_dataframe(db, table, column_list)

if __name__ == "__main__":
    db = sql_reader.connect_to_database('localhost', 'root', 'root', 'SILCK', 33061)
    print(get_skill_list(db))
    print(get_skill_dataframe(db))