# -*- coding: utf-8 -*-
import urllib2
import json
from datetime import datetime, timedelta


def get_holiday(year):
    """
    :param year: 年份
    :return: 所有放假的日期
    """
    baidu_calendar_url = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?query={0}年' \
                         '&co=&resource_id=6018&ie=utf8&oe=utf8'.format(year)
    response = urllib2.urlopen(baidu_calendar_url)
    gmt_format = '%a, %d %b %Y %H:%M:%S GMT'
    print u'北京时间', datetime.strptime(response.headers['Date'], gmt_format) + timedelta(hours=8)
    holiday_list = json.loads(response.read())['data'][0]['holiday']

    # 各个假期放假情况
    holiday_dict = dict()
    # 所有放假的日期
    off_days = set()
    # 调休日
    shift_days = set()

    for holiday in holiday_list:
        single_list = list()
        for day in holiday[u'list']:
            if day[u'status'] == '1':
                single_list.append(day[u'date'])
                off_days.add(day[u'date'])
            if day[u'status'] == '2':
                shift_days.add(day['date'])
        holiday_dict[holiday[u'name']] = single_list

    for (h, d) in holiday_dict.items():
        print h, d

    return off_days

if __name__ == '__main__':
    # 目前只能获取2017当年的数据，往年的api存在变化，只能按月获取
    get_holiday(u'2017')