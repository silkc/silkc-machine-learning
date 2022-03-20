import mysql.connector as mysql_connector
import pandas as pd
from data import sql_reader

def get_aggregated_dataframe(db: mysql_connector.CMySQLConnection) -> pd.DataFrame:
    query = f"SELECT tr.id as training_id, tr.start_at, tr.end_at, " + \
             "tr.total_mark, tr.language as training_language, " + \
             "ts.skill_id as skill_to_train_id, " + \
             "uo.occupation_id practiced_occupation_id, " + \
             "u.id as user_id, " + \
             "u.date_of_birth, u.address, u.up_to_distance, " + \
             "u.professional_experience " + \
             "FROM training tr " + \
             "LEFT JOIN training_skill ts ON tr.id = ts.training_id " + \
             "LEFT JOIN user_training ut ON tr.id = ut.training_id " + \
             "LEFT JOIN occupation_skill os ON os.skill_id = ts.skill_id " + \
             "LEFT JOIN user_occupation uo ON uo.occupation_id = os.id " + \
             "LEFT JOIN user u ON u.id = uo.user_id "

    dataframe = sql_reader.query_to_dataframe(db=db, query=query)
    
    return dataframe
