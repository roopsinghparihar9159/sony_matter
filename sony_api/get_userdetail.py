import requests
import json

# 2309260414064415397
# headers={"Content-Type":"application/json","Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTY2MDM2OTcsImlhdCI6MTY5NjUxNzI5Nywic2NvcGUiOiJhY2Nlc3NfdG9rZW4iLCJzdWIiOiJyYWh1bC5uZW1hZGVAc2V0aW5kaWEuY29tIn0.khBv7wJl_kNl98V--T8LdKVJB8jpBhrvDD_ESggEfSw"}
# result=requests.get("https://pp-da-godavari.sonyliv.com/api/sre_analysis/user_id/190911154297828610?td=2023-10-05%2023%3A00&fd=2023-10-05%2000%3A00",headers=headers)
# print(result.text)
# result_json = result.json()
# print(result_json)
# with open('usersessionebvs_json.json','w') as time_json:
#     json.dump(result_json,time_json)

with open('usersessionebvs_json.json','r') as time_json:
    res_json=json.load(time_json)





# api_resp = api.json()
# for i in res_json['details']:
print(res_json)
# student_details = json.loads(res_json)
# print(dict(student_details))
for i in res_json['details']:
    print(i['vsi'],i['session_start'],i['session_end'])
    # if i['ebvs']==1:
    #     print(i['ebvs'])
    #     print('VSI:',i['vsi'],'START TIME:',i['session_start'],'END TIME:',i['session_end'],'STATUS:',i['status'],'CONTENT ID:',i['content_id'])

