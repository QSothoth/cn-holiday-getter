# -*- coding: utf-8 -*-
import urllib2
import json

baidu_calendar_url = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?query=2017年10月&co=&resource_id=6018&ie=utf8&oe=utf8'
response = urllib2.urlopen(baidu_calendar_url)
holiday_list = json.loads(response.read())['data'][0]['holiday']
off_days = set()
shift_days = set()
for holiday in holiday_list:
    for day in holiday['list']:
        if day['status'] == '1':
            off_days.add(day['date'])
        if day['status'] == '2':
            shift_days.add(day['date'])
print off_days, shift_days