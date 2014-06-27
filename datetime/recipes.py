#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: datetime.recipes.py
Description: this program deals with datatime or time module.
Creation: 2013-11-6
Revision: 2013-11-6
"""
import datetime
import time
import dateutil.parser as parser

#===============================================================================
# Attention:
#     1. can't compare datetime.datetime to datetime.date
#===============================================================================

def seperator(func):
    def actuall_call(*args, **kwargs):
        print "-" * 50
        func(*args, **kwargs)
        print '-' * 50
    return actuall_call
        
#===============================================================================
# convert str object to datetime object

# str objects have different formats：
    # "1998-12-1 00:00:00"
    # "1998-December-1 00:00:00"
    # "1998-Dec-1 00:00:00"
    # "2013-10-1 19:15:55.047000"
# 可以直接使用dateutil来parse,不需要再显示地指定fmt
# dateutil大大简化了从字符串向datetime.datetime的转化
#===============================================================================

date = "1998-12-1 00:00:00"
date_time = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
date_time1 = parser.parse(date)

date = "1998-December-1 00:00:00"
date_time = datetime.datetime.strptime(date, '%Y-%B-%d %H:%M:%S')
date_time2 = parser.parse(date)

date = "1998-Dec-1 00:00:00"
date_time = datetime.datetime.strptime(date, '%Y-%b-%d %H:%M:%S')
date_time3 = parser.parse(date)

date = "2013-10-1 19:15:55.047000"
date_time = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
date_time4 = parser.parse(date)

print date_time1, date_time2, date_time3, date_time4

print '...'
date = '0401'
#print parser.parse(date, dayfirst=True, yearfirst=False)
print datetime.datetime.strptime(date, '%m%d')

#raw_input()

#===============================================================================
# convert datetime object to str object
#===============================================================================

date = date_time.strftime('%Y-%m-%d %H:%M:%S')

#===============================================================================
# calculate the interval between 2 datetime objects
#===============================================================================
date_2 = "1998-12-4 00:00:00"
date_time_2 = datetime.datetime.strptime(date_2, '%Y-%m-%d %H:%M:%S')
difference = date_time_2 - date_time

print difference.days
print difference.seconds
print difference.microseconds
print difference.total_seconds()

print datetime.timedelta(minutes=1).seconds  # 返回结果为60
print datetime.timedelta(hours=1).seconds  # 返回结果为3600
print datetime.timedelta(days=1).seconds  # 返回结果为0
print datetime.timedelta(days=1).total_seconds()  # 返回结果为86400.0

# 下面的3个statements是错误的
# print difference.hours
# print difference.minutes
# print difference.milliseconds

#assert difference.days == 3
#assert date_time < date_time_2

#===============================================================================
# 返回当前时间日期的函数
# 前两个语句基本相似，最后一个只返回当前的日期。
#===============================================================================

print datetime.datetime.now()
print datetime.datetime.today()
print datetime.date.today()

#===============================================================================
# Use max() to get the latest date
#===============================================================================

date_3 = "1999-12-4 00:00:00"
date_time_3 = datetime.datetime.strptime(date_3, '%Y-%m-%d %H:%M:%S')
print max(date_time,
          date_time_2,
          date_time_3)

#===============================================================================
# assert year, month, day
#===============================================================================

year, month, day = 1999, 1, 1
assert 1950 < int(year) < 2100
assert 1 <= int(month) <= 12
assert 1 <= int(day) <= 31

#===============================================================================
# 将时间戳(float)转换成具有可读性的时间格式
#===============================================================================

print "timeStamp"
print time.time()  # float,11位才是小数点
print time.localtime(time.time())  # time.struct_time
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

#===============================================================================
# 测试程序运行时间（microseconds）
# 1. Windows下不用datetime模块作为计时器（经测试发现计时结果不准确）
# 2. 选择time.time(), 不选择time.clock(): 两者都是以秒为单位
#===============================================================================

start = datetime.datetime.now()
elapsed = (datetime.datetime.now() - start).microseconds
print elapsed

#===============================================================================
# 将时间戳(float)转换成datetime格式
#===============================================================================

print datetime.datetime.fromtimestamp(1380453355.047)
print datetime.datetime.fromtimestamp(1402375691.388)
print str(datetime.datetime.fromtimestamp(1402375691.388))
raw_input()
print datetime.date.fromtimestamp(1380453355.047)

#===============================================================================
# 将datetime格式转换成timestamp格式(float)
#===============================================================================

print time.mktime(datetime.datetime.now().timetuple())

#===============================================================================
# 将30分钟转换成timestamp(float)
#===============================================================================

thirty_minutes = datetime.timedelta(minutes=30)
print thirty_minutes.seconds, type(thirty_minutes.seconds)  # int type
print thirty_minutes.total_seconds()

#===============================================================================
# timedelta
#===============================================================================

interval = datetime.timedelta(weeks=40, days=84, hours=23,
                              minutes=50, seconds=600)

print datetime.datetime(1970, 10, 1, 0, 0, 0) + datetime.timedelta(days=2)

#===============================================================================
# 获得datetime object的year, month, day
#===============================================================================

dtime1 = datetime.datetime.now()

print "Current date: ", dtime1.date()
print "Current year: ", dtime1.year
print "Current month: ", dtime1.month
print "Current day: ", dtime1.day

print "The beginning day of the current month of the specified datetime: ", dtime1.replace(day=1)

#===============================================================================
# 判断日期的星期
#===============================================================================

# 返回的是1-7整型数
print dtime1.isoweekday()

#===============================================================================
# 如何能够生成"2014-1-4",而不是"2014-01-04" （只适用于Unix）
#===============================================================================

#print dtime1.strftime("%Y-%-m-%-d")

#===============================================================================
# How to increment datetime month in python
# 如何按月增加日期
#===============================================================================

from dateutil.relativedelta import relativedelta

concerned_date = datetime.datetime.today()
concerned_date = datetime.datetime(1998, 12, 1)
date_after_month = concerned_date + relativedelta(months=1)
print 'Concerned date: ', concerned_date.strftime('%d/%m/%Y')
print 'After Month:', date_after_month.strftime('%d/%m/%Y')

#===============================================================================
# pytz:
#     1. 中国时区使用'Asia/Shanghai',可以从pytz.common_timezones, pytz.all_timezones查阅
#     2. 创建time-zone aware datetime based on a naive datetime object
#     3. 不同时区之间的时间转换
#===============================================================================

import pytz
from pytz import timezone

utc = pytz.utc
china = timezone('Asia/Shanghai')
fmt = '%Y-%m-%d %H:%M:%S %Z%z'

#---创建一个包含时区的datetime对象--- 
# 方法1,从tz-unaware datetime object创建
china_dt = china.localize(datetime.datetime(2002, 10, 27, 6, 0, 0))
print china_dt.strftime(fmt)
# 方法2,从tz-aware datetime object创建 （可以用不同时区时间的转换）
utc_dt = china_dt.astimezone(utc)
print utc_dt.strftime(fmt)
china_dt2 = utc_dt.astimezone(china)
print china_dt2.strftime(fmt)
# 注意：对某些时区，使用tzinfo来创建没有作用。不要使用如下方式：
print datetime.datetime(2002, 10, 27, 12, 0, 0, tzinfo=china)

#---提取出timestamp，并转换成datetime---
# 方法1
fmt = '%Y-%m-%d %H:%M:%S %Z%z'
here_tz = timezone('Asia/Shanghai')
here_dt = pytz.utc.localize(datetime.datetime.utcfromtimestamp(1418313600)).astimezone(here_tz)
print here_dt.strftime(fmt)
# 方法2
print datetime.datetime.fromtimestamp(1418313600)

#===============================================================================
# 实现datetime.datetime和datetime.date之间的转换
#===============================================================================

d1 = datetime.datetime(2013, 1, 1)
d2 = datetime.date(2013, 1, 1)
print d1.date() == d2
print datetime.datetime(d2.year, d2.month, d2.day) == d1