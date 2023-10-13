import pandas as pd
import subprocess
import time
import sqlalchemy
from datetime import datetime
import calendar
import time
from sqlalchemy import create_engine, text

# engine = sqlalchemy.create_engine('mysql+pymysql://root:E4M^ddMm@localhost:3306/RAI_DB1')
# conn = engine.connect()
'''
query = text('SELECT round(avg(time_connect),6) as avg_tm_connect,max(time_connect) as max_tm_connect,round(avg(total_time),6) as avg_total_tm, max(total_time) as max_total_tm,\
round(avg(download_speed),3) as avg_dw_sp, max(download_speed) as max_dw_sp, round(avg(download_size),0) as avg_dw_sz, max(download_size) as max_dw_sz from  curlmonitor1')

df_query = pd.read_sql_query(query,conn)
print('df_query',df_query)
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
    print('**************************************************')
    print(res_dict)
    df = pd.DataFrame([res_dict])

    engine = sqlalchemy.create_engine('mysql+pymysql://root:E4M^ddMm@localhost:3306/RAI_DB1')
    conn = engine.connect()

    df.to_sql(name='curlmonitor',con=engine,index=False,if_exists = 'append')

    df_table = pd.read_sql_table('curlmonitor', conn)
    
    time_conn_avg = df_table['time_connect'].mean()
    time_conn_max = df_table['time_connect'].max()
    total_time_avg = df_table['total_time'].mean()
    total_time_max = df_table['total_time'].max()
    download_speed_avg = df_table['download_speed'].mean()
    download_speed_max = df_table['download_speed'].max()
    download_size_avg = df_table['download_size'].mean()
    download_size_max = df_table['download_size'].max()

    result = f'Time Connect_avg:{time_conn_avg},Time connect max:{time_conn_max},Total time avg: {total_time_avg},Total time max:{total_time_max}'
    print(result)
    result1 = f'Download_speed_avg:{download_speed_avg},Download_speed_max:{download_speed_max},Download_size_avg: {download_size_avg},Download_size_max:{download_size_max}'
    print(result1)

    if float(df['time_connect'])>float(time_conn_avg) and float(df['time_connect'])>float(time_conn_max):
        print("Time connect greater than average and maximum value")
    elif float(df['total_time'])>float(total_time_avg) and float(df['total_time'])>float(total_time_max):
        print("Total time greater than average and maximum value")
    elif float(df['download_speed'])>float(download_speed_avg) and float(df['download_speed'])>float(download_speed_max):
        print("Download speed greater than average and maximum value")
    elif float(df['download_size'])>float(download_size_avg) and float(df['download_size'])>float(download_size_max):
        print("Download Size greater than average and maximum value")
    else:
        print("Situation going on normal....")
    
    time.sleep(10)
