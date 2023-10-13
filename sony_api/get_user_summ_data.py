import requests
import json
from datetime import datetime,timedelta
st = 1692360832814
ed = 1692363803005

sess_st = datetime.utcfromtimestamp(1695949079772/1000)+timedelta(hours=5,minutes=30)
sess_ed = datetime.utcfromtimestamp(1695949084650/1000)+timedelta(hours=5,minutes=30)
st_hour, st_minute, st_second = sess_st.strftime('%H'), sess_st.strftime('%M'), sess_st.strftime('%S')
# print(st_hour, st_minute, st_second)
ed_hour, ed_minute, ed_second = sess_ed.strftime('%H'), sess_ed.strftime('%M'), sess_ed.strftime('%S')
# print(ed_hour, ed_minute, ed_second)
# 1_28_1000065446_1695467179438
headers={"Content-Type":"application/json","Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTYwNjQ4NzIsImlhdCI6MTY5NTk3ODQ3Miwic2NvcGUiOiJhY2Nlc3NfdG9rZW4iLCJzdWIiOiJyYWh1bC5uZW1hZGVAc2V0aW5kaWEuY29tIn0.MfJ3bTVF4YWXk5kUu-rF9ByxugSEm9KWI0T6fC_9Jn8"}
api_link =f"https://pp-da-godavari.sonyliv.com/api/sre_analysis/vsi/1_30_1000241738_1695949079772?td={sess_ed.date()}%20{ed_hour}%3A{ed_minute}&fd={sess_st.date()}%20{st_hour}%3A{st_minute}"
print(api_link)
# api_link=requests.get("https://pp-da-godavari.sonyliv.com/api/sre_analysis/vsi/1_33_1000153451_1695322178466?td=2023-09-22%2023%3A00&fd=2023-09-22%2000%3A00",headers=headers)
result=requests.get(api_link,headers=headers)
print(result.text)
api = result.json()
# print(api)
for i in api:
    if 'summaryData' == i:
        print(api[i]['viewerId'],api[i]['sessionStartTime'],api[i]['sessionEndTime'])
# print(api['summaryData']['viewerId'],api['summaryData']['sessionStartTime'],api['summaryData']['sessionEndTime'])