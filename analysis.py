import pandas as pd
import datetime as dt
from sqlalchemy import create_engine, text

engine = create_engine('sqlite:///generator.db')

def read_db(query:str,params:dict={}) -> pd.DataFrame:
    '''
    reads the database using SQL Alchemy based on query and returns a DataFrame
    '''
    parsed = text(query)
    with engine.connect() as conn:
        df = pd.read_sql_query(parsed,conn,params=params)
    return df


def outliers(min:pd.DataFrame,reg:pd.DataFrame) -> pd.DataFrame:
    '''
    gets the previous and next value based on an outlier and creates a dataframe
    '''
    ids = []
    speeds = []
    tmstps = []
    for id,speed,timestamp in zip(min['id'].values,min['speed'].values,min['timestamp'].values):
        id_min_one = reg[reg['id'] == id-1]
        id_plu_one = reg[reg['id'] == id+1]
        for _id,_speed,_timestamp in zip(id_min_one['id'].values,id_min_one['speed'].values,id_min_one['timestamp'].values):
            ids.append(_id)
            speeds.append(_speed)
            tmstps.append(dt.datetime.strptime(_timestamp,"%Y-%m-%d %H:%M:%S"))
        ids.append(id)
        speeds.append(speed)
        tmstps.append(dt.datetime.strptime(timestamp,"%Y-%m-%d %H:%M:%S"))
        for id_,speed_,timestamp_ in zip(id_plu_one['id'].values,id_plu_one['speed'].values,id_plu_one['timestamp'].values):
            ids.append(id_)
            speeds.append(speed_)
            tmstps.append(dt.datetime.strptime(timestamp_,"%Y-%m-%d %H:%M:%S"))

    result = pd.DataFrame()
    result.insert(0,'id',ids)
    result.insert(1,'speed',speeds)
    result.insert(2,'timestamp',tmstps)
    return result



# df.info()
# print(df.head())