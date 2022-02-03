import mysql.connector as mysql_connector
import pandas as pd
from data import sql_reader

debug: bool = True
limit: int = 750

def get_aggregated_dataframe(db: mysql_connector.CMySQLConnection) -> pd.DataFrame:

    query = f"SELECT occupation.id, occupation.preferred_label, occupation.hidden_labels, occupation.description, " + \
       "isco_group.concept_type, isco_group.code, isco_group.preferred_label AS isco_preferred_label, " + \
       "isco_group.description AS isco_description, occupation_skill.relation_type, occupation_skill.skill_type, " + \
       "training.description AS training_description, training.is_online, training.name, training_skill.is_required, training_skill.is_to_acquire " + \
        "FROM occupation JOIN isco_group JOIN occupation_skill JOIN training JOIN training_skill " + \
        "WHERE occupation.isco_group_id = isco_group.id or occupation_skill.occupation_id = occupation.id or training_skill.training_id = training.id"
    dataframe = sql_reader.query_to_dataframe(db=db, query=query)

    return dataframe

def get_aggregate_dataframe(db: mysql_connector.CMySQLConnection) -> pd.DataFrame:
    #TODO get values from view

    # drop aggregate view if exist
    query = 'DROP VIEW IF EXISTS aggregate'
    sql_reader.execute_query(db, query)
    # create aggregate view
    query = f'CREATE VIEW aggregate AS \n' + \
            "SELECT occupation.id, occupation.preferred_label AS occupation_preferred_label, occupation.hidden_labels, occupation.description AS occupation_description, " + \
            "isco_group.concept_type, isco_group.code, isco_group.preferred_label AS isco_preferred_label, " + \
            "isco_group.description AS isco_group_description, occupation_skill.relation_type, occupation_skill.skill_type AS occupation_skill_skill_type, " + \
            "training.description AS training_description, training.is_online, training.name, training_skill.is_required, training_skill.is_to_acquire " + \
            "FROM occupation JOIN isco_group JOIN occupation_skill JOIN training JOIN training_skill " + \
            "WHERE occupation.isco_group_id = isco_group.id or occupation_skill.occupation_id = occupation.id or training_skill.training_id = training.id"
    sql_reader.execute_query(db, query)
    if debug:
        query = f'SELECT * FROM aggregate LIMIT {limit}'
    else:
        query = 'SELECT * FROM aggregate'
    dataframe = sql_reader.query_to_dataframe(db, query)
    return dataframe

if __name__ == "__main__":
    db = sql_reader.connect_to_database('localhost', 'root', 'root', 'silck', 8889)
    #print(get_aggregated_dataframe(db))
    print(get_aggregate_dataframe(db))
