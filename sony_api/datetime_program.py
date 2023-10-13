import math
import calendar
from datetime import datetime, timedelta
five_hours_from_now = datetime.now()

print(five_hours_from_now)

five_hours_minutes = datetime.now() + timedelta(hours=5,minutes=30)
print(five_hours_minutes)

time_only = (datetime.now() + timedelta(hours=5,minutes=30)).strftime('%H:%M:%S')

print(time_only)

last30day = (datetime.now() + timedelta(days=-30)).strftime('%Y-%m-%d %H:%M:%S')
print('last 30 days',last30day)

next_date = last30day = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
print('next date',next_date)

# t=datetime.datetime(2021, 7, 7, 1, 2, 1)
today = datetime.now()
print('today date',type(today))
epoch = calendar.timegm(today.timetuple())
print(epoch)
abs_res = math.trunc(abs(1694540124916/1000))
print(abs_res)
epoch_date_time = datetime.utcfromtimestamp(1683646092)
raitime = '2023-05-09 15:28:12'
p = datetime.strptime(raitime, '%Y-%m-%d %H:%M:%S')

epoch = calendar.timegm(p.timetuple())
print('epoch_date_time',epoch)

print("Given epoch time:", epoch)
print("Converted Datetime:", epoch_date_time)

# for linux only
epoch1 = today.strftime('%s')

print(epoch1)

# ************************************************************
print("*********************************************************************")
epoch_date_time = datetime.utcfromtimestamp(1692360832814/1000)+timedelta(hours=5,minutes=30)
print('datetime:',epoch_date_time.date())
print('Year:',epoch_date_time.year)
print('Month:',epoch_date_time.month)
print('Day:',epoch_date_time.day)
print('Hour:',epoch_date_time.hour)
print('Minute:',epoch_date_time.minute)
print('Second:',epoch_date_time.second)
