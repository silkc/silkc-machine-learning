import mysql.connector as mysql_connector
import pandas as pd
from data import sql_reader

def get_aggregated_dataframe(db: mysql_connector.CMySQLConnection) -> pd.DataFrame:
        
    query = f"SELECT GROUP_CONCAT(DISTINCT(tr.id)) as training_id, tr.euro_price, tr.start_at, tr.end_at, tr.is_online, " + \
            "tr.is_online_monitored, tr.is_presential, tr.score, tr.longitude, tr.latitude, " + \
            "tr.duration_time_to_seconds, tr.avg_mark, tr.total_mark, tr.language, " + \
            "tr.is_certified," + \
            "os.occupation_id as skill_occupation_id, os.skill_id, os.relation_type " + \
            "FROM training tr LEFT JOIN training_skill ts ON tr.id = ts.training_id " + \
            "LEFT JOIN occupation_skill os ON ts.skill_id = os.skill_id " + \
            "WHERE os.occupation_id IS NOT NULL GROUP BY tr.id"

    
    dataframe = sql_reader.query_to_dataframe(db=db, query=query)
    
    return dataframe
