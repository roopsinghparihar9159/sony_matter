import pandas as pd
import sqlalchemy
from datetime import datetime
import calendar
import time
from sqlalchemy import create_engine, text

engine = sqlalchemy.create_engine('mysql+pymysql://root:E4M^ddMm@localhost:3306/RAI_DB1')
conn = engine.connect()
df_table = pd.read_sql_table('curlmonitor1', conn)

# print(df_table.head())
# print(df_table.shape)
cols = ['time_connect','total_time','download_speed','download_size']
df_table[cols] = df_table[cols].apply(pd.to_numeric,errors='coerce', axis=1)

print(df_table.info())

# print(df_table['time_connect'].mean(),df_table['time_connect'].max())
df_dict = dict()
df_dict['time_conn_avg'] = df_table['time_connect'].mean()
df_dict['time_conn_max'] = df_table['time_connect'].max()
df_dict['total_time_avg'] = df_table['total_time'].mean()
df_dict['total_time_max'] = df_table['total_time'].max()
df_dict['download_speed_avg'] = df_table['download_speed'].mean()
df_dict['download_speed_max'] = df_table['download_speed'].max()
df_dict['download_size_avg'] = df_table['download_size'].mean()
df_dict['download_size_max'] = df_table['download_size'].max()

print(df_dict)
print(type(df_dict['time_conn_avg']))
