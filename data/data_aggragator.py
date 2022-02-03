import mysql.connector as mysql_connector
import pandas as pd
import sql_reader

def get_aggregated_dataframe(db: mysql_connector.CMySQLConnection) -> pd.DataFrame:

    query = f"SELECT occupation.id, occupation.preferred_label, occupation.hidden_labels, occupation.description, " + \
       "isco_group.concept_type, isco_group.code, isco_group.preferred_label AS isco_preferred_label, " + \
       "isco_group.description AS isco_description, occupation_skill.relation_type, occupation_skill.skill_type, " + \
       "training.description AS training_description, training.is_online, training.name, training_skill.is_required, training_skill.is_to_acquire " + \
        "FROM occupation JOIN isco_group JOIN occupation_skill JOIN training JOIN training_skill " + \
        "WHERE occupation.isco_group_id = isco_group.id or occupation_skill.occupation_id = occupation.id or training_skill.training_id = training.id"
    dataframe = sql_reader.query_to_dataframe(db=db, query=query)

    return dataframe

if __name__ == "__main__":
    db = sql_reader.connect_to_database('localhost', 'root', 'marcosql2022', 'silck', 3306)
    print(get_aggregated_dataframe(db))