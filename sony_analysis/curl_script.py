import pandas as pd
import subprocess
import time
import sqlalchemy
from datetime import datetime
import calendar
import time
from sqlalchemy import create_engine, text

engine = sqlalchemy.create_engine('mysql+pymysql://root:E4M^ddMm@localhost:3306/RAI_DB1')
conn = engine.connect()
'''
query = text('SELECT round(avg(time_connect),6) as avg_tm_connect,max(time_connect) as max_tm_connect,round(avg(total_time),6) as avg_total_tm, max(total_time) as max_total_tm,\
round(avg(download_speed),3) as avg_dw_sp, max(download_speed) as max_dw_sp, round(avg(download_size),0) as avg_dw_sz, max(download_size) as max_dw_sz from  curlmonitor')

df_query = pd.read_sql_query(query,conn)
print(df_query)
'''

# df_table = pd.read_sql_table('curlmonitor', conn)


url = "curl https://sony247channels.akamaized.net/hls/live/2011671/SETHD/master.m3u8?hdnea=st=1666483270~exp=1718323270~acl=/*~hmac=0b6d53622b73b15df03a3c3f55d6966442882d9a95c10d6a7f375f1a02801f6e -w 'time_connect: %{time_connect},total_time:%{time_total},download_speed:%{speed_download},http_code:%{http_code},download_size:%{size_download}' -o /dev/null"
while True:
    proc = subprocess.Popen([url], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    result = out
    output = result.decode()
    res_split = output.split(',')
    collection_list = list()
    for val in res_split:
        res_colon_split = val.split(':')
        collection_list.append(res_colon_split)
    res_dict = dict(collection_list)
    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)
    dt_object = datetime.fromtimestamp(time_stamp)
    res_dict['timestamp'] = dt_object
    print(res_dict)

    query = text('SELECT round(avg(time_connect),6) as avg_tm_connect,max(time_connect) as max_tm_connect,round(avg(total_time),6) as avg_total_tm, max(total_time) as max_total_tm,\
        round(avg(download_speed),3) as avg_dw_sp, max(download_speed) as max_dw_sp, round(avg(download_size),0) as avg_dw_sz, max(download_size) as max_dw_sz from  curlmonitor1')

    df_query = pd.read_sql_query(query,conn)
    print(df_query)

    if float(res_dict['time_connect'])>float(df_query['avg_tm_connect']) and float(res_dict['time_connect'])>float(df_query['max_tm_connect']):
        # print(float(res_dict['time_connect']))
        print("Time connect greater than average and maximum value")
    elif float(res_dict['total_time'])>float(df_query['avg_total_tm']) and float(res_dict['total_time'])>float(df_query['max_total_tm']):
        # print(float(res_dict['total_time']))
        print("Total time greater than average and maximum value")
    elif float(res_dict['download_speed'])>float(df_query['avg_dw_sp']) and float(res_dict['download_speed'])>float(df_query['max_dw_sp']):
        # print(float(res_dict['download_speed']))
        print("Download speed greater than average and maximum value")
    elif float(res_dict['download_size'])>float(df_query['avg_dw_sz']) and float(res_dict['download_size'])>float(df_query['max_dw_sz']):
        # print(float(res_dict['download_size']))
        print("Download Size greater than average and maximum value")
    else:
        print("Situation going on normal....")
    
    df = pd.DataFrame([res_dict])
    df.to_sql(name='curlmonitor1',con=engine,index=False,if_exists = 'append')
    time.sleep(60)
