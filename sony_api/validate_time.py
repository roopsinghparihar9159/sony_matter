import calendar
from datetime import datetime, timedelta
import time
from generate_token import *

today = datetime.now()
print('today date',today)
current_epoch = calendar.timegm(today.timetuple())
print(current_epoch)

current_time = today.strftime('%H:%M:%S')
print('current time:',current_time)

# epoch_time = calendar.timegm(current_time.timetuple())
# print('Epoch time:',epoch_time)

import datetime
import dateutil.relativedelta

with open("token.json", "r") as token_file:
    res_json=json.load(token_file)
# print(res_json)
token_epoch = res_json['epoch']
# print('Token epoch:',token_epoch)

dt1 = datetime.datetime.fromtimestamp(token_epoch) # 1973-11-29 22:33:09
dt2 = datetime.datetime.fromtimestamp(current_epoch) # 1977-06-07 23:44:50
rd = dateutil.relativedelta.relativedelta (dt2, dt1)

print("%d years, %d months, %d days, %d hours, %d minutes and %d seconds" % (rd.years, rd.months, rd.days, rd.hours, rd.minutes, rd.seconds))
# 3 years, 6 months, 9 days, 1 hours, 11 minutes and 41 seconds
total_second = rd.minutes*60
print('Total Second:',total_second)
# new_token = get_newtoken()
# print(new_token)
# token_epoch = new_token['epoch']



if total_second > 900:
    new_token = get_newtoken()
    token = new_token['token']
    print('New Token',token)
    print('New Token Generated')
else:
    token=res_json['token']
    print('Old Token:',token)
    print('Time not expired')