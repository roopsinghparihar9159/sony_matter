import os
import calendar
from datetime import datetime,timedelta
import math
import hashlib
import mysql.connector as sql
import json
# from function import getCacheDir
import requests
from requests.exceptions import HTTPError
date_ = datetime.today().strftime('%Y-%m-%d')
print(date_)
ec = 'ACN01'
ecMd5Str = hashlib.md5(ec.encode()).hexdigest()
print(ecMd5Str)
# sql_query = "select * from rai_analysis.dailydata where hashlib.md5(errorCode.encode()).hexdigest()='"+ ecMd5Str +"' and date_format(inserted_at,'%Y-%m-%d') = '"+ date_ + "'limit 10"

# sql_query = "select * from rai_analysis.dailydata where errorCode='"+ ec +"' and date_format(inserted_at,'%Y-%m-%d') = '"+ date_ + "'"
sql_query = "SELECT userid, userIdentifier,timestamp FROM dailydata1 where errorcode='ACN01' and timestamp between '2023-08-07 00:00:00' and '2023-08-07 23:59:59';"

db_connection = sql.connect(host='localhost', port= '3306', database='django', user='root', password='E4M^ddMm')
db_cursor = db_connection.cursor(dictionary=True)
db_cursor.execute(sql_query)
table_rows = db_cursor.fetchall()
# print(table_rows,"----\n\n")
# Get user all the sessions
for d in table_rows:
    print(d['userIdentifier'])
    headers={"Content-Type":"application/json","Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTYwNTQxNDcsImlhdCI6MTY5NTk2Nzc0Nywic2NvcGUiOiJhY2Nlc3NfdG9rZW4iLCJzdWIiOiJyYWh1bC5uZW1hZGVAc2V0aW5kaWEuY29tIn0.0vnXLZo5oX4HKX_PPti-8XGfHBHBVlkv5dHSbyKv0nI"}
    result=requests.get(f"https://pp-da-godavari.sonyliv.com/api/sre_analysis/user_id/{d['userIdentifier']}?td=2023-08-07%2023%3A59&fd=2023-08-07%2000%3A00",headers=headers)
    # print(result.text)
    user_session = result.json()
    for i in user_session['details']:
        print("getting user session data")
        print(i['vsi'],i['session_start'],i['session_end'])
        print("end user session data")
        # Get user summary data
        sess_st = datetime.utcfromtimestamp(i['session_start'] / 1000) + timedelta(hours=5, minutes=30)
        sess_ed = datetime.utcfromtimestamp(i['session_end'] / 1000) + timedelta(hours=5, minutes=30)
        st_hour, st_minute, st_second = sess_st.strftime('%H'), sess_st.strftime('%M'), sess_st.strftime('%S')
        # print(st_hour, st_minute, st_second)
        ed_hour, ed_minute, ed_second = sess_ed.strftime('%H'), sess_ed.strftime('%M'), sess_ed.strftime('%S')
        # print(ed_hour, ed_minute, ed_second)
        try:
            api_link = f"https://pp-da-godavari.sonyliv.com/api/sre_analysis/vsi/{i['vsi']}?td={sess_ed.date()}%20{ed_hour}%3A{ed_minute}&fd={sess_st.date()}%20{st_hour}%3A{st_minute}"
            result = requests.get(api_link, headers=headers)
            api = result.json()
            for i in api:
                if 'summaryData' == i:
                    print("start user summary data")
                    print(api[i]['viewerId'], api[i]['sessionStartTime'], api[i]['sessionEndTime'])
                    print("end user summary data")
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')