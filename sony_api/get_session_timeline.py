import requests
import json
from datetime import datetime,timedelta
st = 1696963735336-10000
ed = 1696963739977+10000
# session_id = 1_28_1000163209_1696963735336
# 1696963725336
# 1696963749977
sess_st = datetime.utcfromtimestamp(st/1000)+timedelta(hours=5,minutes=30)
sess_ed = datetime.utcfromtimestamp(ed/1000)+timedelta(hours=5,minutes=30)
st_hour, st_minute, st_second = sess_st.strftime('%H'), sess_st.strftime('%M'), sess_st.strftime('%S')
print(st_hour, st_minute, st_second)
ed_hour, ed_minute, ed_second = sess_ed.strftime('%H'), sess_ed.strftime('%M'), sess_ed.strftime('%S')
print(ed_hour, ed_minute, ed_second)
# 1_28_1000065446_1695467179438
headers={"Content-Type":"application/json","Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTcxNzgzNjgsImlhdCI6MTY5NzA5MTk2OCwic2NvcGUiOiJhY2Nlc3NfdG9rZW4iLCJzdWIiOiJyYWh1bC5uZW1hZGVAc2V0aW5kaWEuY29tIn0.lri_aXat5fvw6zjpG9rv5LtddmUWpLp1FgexbTVUQFg"}
api_link =f"https://pp-da-godavari.sonyliv.com/api/sre_analysis/vsi_events/1_28_1000163209_1696963735336?td={sess_ed.date()}%20{ed_hour}%3A{ed_minute}&fd={sess_st.date()}%20{st_hour}%3A{st_minute}"
print(api_link)
# api_link=requests.get("https://pp-da-godavari.sonyliv.com/api/sre_analysis/vsi/1_28_1000163209_1696963735336?td=2023-09-22%2023%3A00&fd=2023-09-22%2000%3A00",headers=headers)
result=requests.get(api_link,headers=headers)

print(result.text)
# result_json = result.json()
# print(result_json)
# with open('timeline_json.json','w') as time_json:
#     json.dump(result_json,time_json)