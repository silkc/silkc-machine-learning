import mysql.connector as mysql_connector
import pandas as pd

def connect_to_database(host:str, username:str, password:str, database_name:str = None) -> mysql_connector.CMySQLConnection:
    if database_name is None:
        db = mysql_connector.connect(host=host, username=username, password=password)
    else:
        db = mysql_connector.connect(host=host, username=username, password=password, database=database_name)

    return db

def read_sql_data_to_list(db:mysql_connector.CMySQLConnection, table:str, column_list:str = '*') -> list:
    #%% get the curso
    cursor = db.cursor()
    #%% define the query
    query = f"SELECT {column_list} FROM {table}"
    #%% execute query
    cursor.execute(query)
    #%% getting record from the record
    record = cursor.fetchall()
    return record

def read_sql_data_to_dataframe(db: mysql_connector.CMySQLConnection, table:str, column_list:str = '*') -> pd.DataFrame:
    # %% define the query
    query = f"SELECT {column_list} FROM {table}"
    dataframe = pd.read_sql(query, db)
    return dataframe

if __name__ == "__main__":
    connect_to_database('localhost', 'root', 'marcosql2021')
    db = connect_to_database('localhost', 'root', 'marcosql2021', 'silck')
    print(read_sql_data_to_list(db, 'skill'))