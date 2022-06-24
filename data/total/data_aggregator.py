import mysql.connector as mysql_connector
import pandas as pd
from data import sql_reader
from data import skill_data_reader

def get_aggregated_dataframe(db: mysql_connector.CMySQLConnection) -> pd.DataFrame:
    query = f"SELECT Training.id AS training_id, IFNULL(TS.skill_id, 0) AS skill_id, User.id AS user_id, " + \
    "IF(US.id IS NOT NULL OR SQ1.trainings_ids IS NOT NULL OR SQ2.occupations_ids IS NOT NULL, 1, 0) AS is_acquired, " + \
    "IF(US.id IS NOT NULL, 1, 0) AS is_acquired_by_skill, " + \
    "IF(SQ1.trainings_ids IS NOT NULL, 1, 0) AS is_acquired_by_training, " + \
    "IF(SQ1.trainings_ids IS NOT NULL, SQ1.trainings_ids, 0) AS skill_acquired_by_training_ids, " + \
    "IF(SQ2.occupations_ids IS NOT NULL, 1, 0) AS is_acquired_by_occupation, " + \
    "IF(SQ2.occupations_ids IS NOT NULL, SQ2.occupations_ids, 0) AS acquired_by_occupation_ids, " + \
    "User.date_of_birth, User.address, User.professional_experience, User.longitude, User.latitude " + \
    "FROM training AS Training " + \
    "LEFT JOIN training_skill AS TS ON TS.training_id = Training.id CROSS JOIN user AS User LEFT JOIN user_skill AS US ON US.user_id = User.id AND US.skill_id = TS.skill_id LEFT JOIN (" + \
    "SELECT " + \
        "UT.user_id," + \
        "TS.skill_id,"  + \
        "GROUP_CONCAT(DISTINCT(UT.training_id)) AS trainings_ids " + \
    "FROM user_training AS UT " + \
    "INNER JOIN training_skill AS TS ON TS.training_id = UT.training_id AND TS.is_to_acquire = 1 " + \
    "WHERE UT.is_followed = 1 " + \
    "GROUP BY UT.user_id, TS.skill_id " + \
") AS SQ1 ON SQ1.user_id = User.id AND SQ1.skill_id = TS.skill_id LEFT JOIN (" + \
    "SELECT " + \
        "UO.user_id," + \
        "OS.skill_id,"  + \
        "GROUP_CONCAT(DISTINCT(UO.occupation_id)) AS occupations_ids " + \
    "FROM user_occupation AS UO " + \
    "LEFT JOIN occupation_skill AS OS ON OS.occupation_id = UO.occupation_id AND OS.skill_type = 'skill/competence' AND OS.relation_type = 'essential' " + \
    "WHERE (UO.is_current = 1 OR UO.is_previous = 1) AND OS.id IS NOT NULL " + \
    "GROUP BY UO.user_id, OS.skill_id " + \
") AS SQ2 ON SQ2.user_id = User.id AND SQ2.skill_id = TS.skill_id ORDER BY Training.id, TS.skill_id, User.id"

    dataframe = sql_reader.query_to_dataframe(db=db, query=query)
    
    #dataframe = dataframe[dataframe['is_acquired_by_training'] == 1]
    
    unique_user = dataframe.user_id.unique()
    
    columns=['user_id', 'training_ids']
    
    skill_ids = skill_data_reader.get_skill_id(db=db)
    
    for s in skill_ids:
        columns.append('skill_' + str(s[0]))
    
    dataframe2 = pd.DataFrame(columns=columns)
    
    for uid in unique_user:
        dt = dataframe[dataframe['user_id'] == uid]
        skill_list = dt.skill_id.unique()
        training_list = dt.training_id.unique()
        training_ids = ','.join(map(str, training_list))
        
        row = {'user_id': uid, 'training_ids': training_ids}
        
        for s in skill_list:
            row['skill_' + str(s)] = s
        
        for s in set(skill_ids)-set(skill_list):
            row['skill_' + str(s[0])] = 0
        
        dataframe2 = dataframe2.append(row, ignore_index=True)
    
    return dataframe2