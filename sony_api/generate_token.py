import requests
import calendar
from datetime import datetime, timedelta
import json
# headers={"Content-Type":"application/json","name":"Rahul","email":"rahul.nemade@setindia.com"}
# result=requests.get("https://pp-da-godavari.sonyliv.com/api/get_token",headers=headers)
#
# print(result.text)8000

def get_newtoken():
    headers = {"Content-Type": "application/json", "name": "Rahul", "email": "rahul.nemade@setindia.com"}
    result=requests.get("https://pp-da-godavari.sonyliv.com/api/get_token",headers=headers)
    result_json = result.json()
    today = datetime.now()
    # print('today date', today)
    epoch = calendar.timegm(today.timetuple())
    # print(epoch)
    # print(result.text)
    # print(result_json)
    token_dict = {}
    token_dict['token'] = result_json['token']
    token_dict['epoch'] = epoch
    with open("token.json", "w") as token_file:
        json.dump(token_dict, token_file)
    return token_dict

print(get_newtoken())