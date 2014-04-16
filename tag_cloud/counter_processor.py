#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: tag_cloud.tag_creator.py
Creation: 2013-12-31
Revision: 2013-12-31
"""

import codecs
import datetime
import os
import sys

from collections import defaultdict
from pprint import pprint
from preprocessor import get_date_time
from file_system import (get_entity_extractor_sorted_fpath,
                         COUNTERS)
from utils import (is_monday,
                   get_time_period_for_mon)

NINE_HOURS = datetime.timedelta(hours=9)
FIFTEEN_HOURS = datetime.timedelta(hours=15)
EIGHTEEN_HOURS = datetime.timedelta(hours=18)
ONE_DAY = datetime.timedelta(days=1)

#===============================================================================
# 主函数
#===============================================================================

def process_counter(current_dir, concerned_date):
    ofpath = get_entity_extractor_sorted_fpath(current_dir, concerned_date)

    if is_monday(concerned_date):
        get_counters_for_mon(ofpath, current_dir, concerned_date)
    else:
        get_counters(ofpath, current_dir)

#===============================================================================
# 处理周一的数据，包含了周五下午3点至周一早上9点的所有数据
#===============================================================================

def get_counters_for_mon(fname, current_dir, concerned_date):
    nine_am_in_mon, three_pm_in_fri = get_time_period_for_mon(concerned_date)
    companies_in_one_day = defaultdict(lambda: 0)
    tags_in_one_day = defaultdict(lambda: 0)

    with open(fname) as f:
        for i, line in enumerate(f):
            if i == 0 and line[:3] == codecs.BOM_UTF8:
                line = line[3:]

            splitted = line.strip("\n").split("|")

            # 从每一条记录提取所有字段
            _news_id = splitted[0]
            date = splitted[1]
            companies = splitted[2]
            companies = list(set(each.split(":")[0] for each in companies.split(";")))
            tags = splitted[3]
            tags = list(set(each.split(":")[0] for each in tags.split(";")))

            # 字符串格式时间转换成datetime objects
            date_time = get_date_time(date)

            if (date_time > three_pm_in_fri and
                date_time < nine_am_in_mon):
                for comp in companies:
                    if not comp:
                        continue
                    companies_in_one_day[comp] += 1
                for tag in tags:
                    if not tag:
                        continue
                    tags_in_one_day[tag] += 1

    save_counters(concerned_date, companies_in_one_day,
                  tags_in_one_day, current_dir)


#===============================================================================
# 生成3:00pm ~ 9:00am (the second day)的词云
# 对处理的数据有一个要求：
#     1.以天为粒度保证最
#===============================================================================

def get_counters(fname, current_dir):
    print fname
    latest_date, _oldest_date = get_latest_and_oldest_date(fname)
    #print latest_date, oldest_date

    # 初始化
    later = latest_date + NINE_HOURS
    older = later - EIGHTEEN_HOURS
    #print later, older

    companies_in_one_day = defaultdict(lambda: 0)
    tags_in_one_day = defaultdict(lambda: 0)

    with open(fname) as f:
        for i, line in enumerate(f):
            if i == 0 and line[:3] == codecs.BOM_UTF8:
                line = line[3:]

            splitted = line.strip("\n").split("|")

            # 从每一条记录提取所有字段
            _news_id = splitted[0]
            date = splitted[1]
            companies = splitted[2]
            companies = list(set(each.split(":")[0] for each in companies.split(";")))
            tags = splitted[3]
            tags = list(set(each.split(":")[0] for each in tags.split(";")))

            # 字符串格式时间转换成datetime objects
            date_time = get_date_time(date)
            #print date_time

            # 处理每天的记录
            if date_time > later:
                continue
            elif older < date_time <= later:
                for comp in companies:
                    if not comp:
                        continue
                    companies_in_one_day[comp] += 1
                for tag in tags:
                    if not tag:
                        continue
                    tags_in_one_day[tag] += 1
            else:
                save_counters(later, companies_in_one_day,
                              tags_in_one_day, current_dir)
                later, older = update_later_and_older_dtime(later, older)
                companies_in_one_day = defaultdict(lambda: 0)
                tags_in_one_day = defaultdict(lambda: 0)
        else:
            save_counters(later, companies_in_one_day,
                          tags_in_one_day, current_dir)

def get_latest_and_oldest_date(fname):
    with open(fname) as f:
        for line in f:
            # 提取文件最近的日期
            date = line.split("|")[1]
            date_time = get_date_time(date)
            latest = date_time.replace(hour=0, minute=0, second=0)

            # 提取文件最早的日期
            oldest = latest.replace(day=1)
            return latest, oldest

def update_later_and_older_dtime(later, older):
    later_updated = later - ONE_DAY
    older_updated = older - ONE_DAY
    return later_updated, older_updated

def save_counters(later, companies_in_one_day,
                  tags_in_one_day, current_dir):
    if isinstance(later, datetime.datetime):
        str_later = later.strftime('%Y-%-m-%-d')
    else:
        str_later = later
    fname = "".join([str_later, ".txt"])

    companies_fpath, tags_fpath = [os.path.join(current_dir, each, fname) for each in COUNTERS]

    with open(companies_fpath, "w") as wf1:
        for (k1, v1) in sorted(companies_in_one_day.items(), key=lambda k: k[1], reverse=True):
            wf1.write("::".join([k1, str(v1)]) + "\n")

    with open(tags_fpath, "w") as wf2:
        for (k2, v2) in sorted(tags_in_one_day.items(), key=lambda k: k[1], reverse=True):
            wf2.write("::".join([k2, str(v2)]) + "\n")
