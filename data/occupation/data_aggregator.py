import mysql.connector as mysql_connector
import pandas as pd
from data import sql_reader

def get_aggregated_dataframe(db: mysql_connector.CMySQLConnection) -> pd.DataFrame:
    query = f"SELECT tr.id as training_id, tr.start_at, tr.end_at, " + \
            "tr.total_mark, tr.language as training_language, " + \
            "os.occupation_id as skill_occupation_id, " + \
            "os.skill_id, " + \
            "os.relation_type " + \
            "FROM training tr " + \
            "LEFT JOIN training_skill ts ON tr.id = ts.training_id " + \
            "LEFT JOIN occupation_skill os ON ts.skill_id = os.skill_id " + \
            "WHERE os.occupation_id IS NOT NULL"
    dataframe = sql_reader.query_to_dataframe(db=db, query=query)
    
    return dataframe
