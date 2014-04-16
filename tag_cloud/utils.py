#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: tag_cloud.utils.py
Description: this program gives utilities.
Creation: 2014-1-13
Revision: 2014-1-13
"""

import datetime

#===============================================================================
# 判断日期是否是星期一
#===============================================================================

def is_monday(date_str):
    flag = False
    dtime = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    
    if dtime.isoweekday() == 1:
        flag = True
    
    return flag

def get_time_period_for_mon(date_str):
    dtime = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    
    # 星期一早上9点
    nine_am_in_mon = dtime + datetime.timedelta(hours=9)
    # 周五下午3点
    three_pm_in_fri = dtime - datetime.timedelta(days=2, hours=9)
    
    return nine_am_in_mon, three_pm_in_fri


if __name__ == "__main__":
    
    print (is_monday("2014-1-13"))
    print get_time_period_for_mon("2014-1-13")
