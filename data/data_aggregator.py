import mysql.connector as mysql_connector
import pandas as pd
from data import sql_reader

debug: bool = False
limit: int = 0

def get_aggregated_dataframe(db: mysql_connector.CMySQLConnection) -> pd.DataFrame:

    # Get data on the association of skills, occupations, trainings and users.
    # We do not get into details such as the score given by other users to a training
    # or the previous searches or skills of other, similar, users. Other information like
    # the list of jobs and trainings of other users is already available.
    
    query = f'SELECT tr.id as training_id, tr.euro_price, tr.start_at, tr.end_at,' + \
                'tr.is_online, tr.is_online_monitored, tr.is_presential, tr.score, tr.longitude, tr.latitude,' + \
                'tr.duration_time_to_seconds, tr.avg_mark, tr.total_mark, tr.language, tr.is_certified,' + \
                'ut.user_id, uo.occupation_id as user_occupation_id,' + \
                'os.occupation_id as skill_occupation_id, os.skill_id, os.relation_type' + \
            'FROM training tr JOIN training_skill ts ON tr.id = ts.training_id' + \
                'JOIN occupation_skill os ON ts.skill_id = os.skill_id' + \
                'JOIN user_training ut ON tr.id = ut.training_id' + \
                'JOIN user_occupation uo ON ut.user_id = uo.user_id'
    # "WHERE tr.is_validated = 1 AND tr.is_rejected = 0"
    dataframe = sql_reader.query_to_dataframe(db=db, query=query)

    return dataframe

def get_aggregate_dataframe(db: mysql_connector.CMySQLConnection) -> pd.DataFrame:
    # drop aggregate view if exist
    query = 'DROP VIEW IF EXISTS aggregate'
    sql_reader.execute_query(db, query)
    # create aggregate view
    query = f'CREATE VIEW aggregate AS \n' + \
             "SELECT tr.id as training_id, tr.euro_price, tr.start_at, tr.end_at, tr.is_online, " + \
             "tr.is_online_monitored, tr.is_presential, tr.score, tr.longitude, tr.latitude, " + \
             "tr.duration_time_to_seconds, tr.avg_mark, tr.total_mark, tr.language, " + \
             "tr.is_certified, ut.user_id, uo.occupation_id as user_occupation_id, " + \
             "os.occupation_id as skill_occupation_id, os.skill_id, os.relation_type " + \
             "FROM training tr LEFT JOIN training_skill ts ON tr.id = ts.training_id " + \
             "LEFT JOIN occupation_skill os ON ts.skill_id = os.skill_id " + \
             "LEFT JOIN user_training ut ON tr.id = ut.training_id " + \
             "LEFT JOIN user_occupation uo ON ut.user_id = uo.user_id "
    #"WHERE tr.is_validated = 1 AND tr.is_rejected = 0"
    sql_reader.execute_query(db, query)
    if debug:
        query = f'SELECT * FROM aggregate LIMIT {limit}'
    else:
        query = 'SELECT * FROM aggregate'
    dataframe = sql_reader.query_to_dataframe(db, query)
    return dataframe

if __name__ == "__main__":
    db = sql_reader.connect_to_database('localhost', 'root', 'root', 'silck', 8889)
    #print(get_aggregated_dataframe(db)) # Select
    print(get_aggregate_dataframe(db)) # View
