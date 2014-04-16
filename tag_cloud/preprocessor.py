#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: tag_cloud.preprocessor.py
Creation: 2014-1-2
Revision: 2014-1-2
"""

import os
import sys
#===============================================================================
# 对时间戳数据进行预处理，保证新闻能够以时间先后顺序出现
#===============================================================================

import datetime
from file_system import (get_entity_extractor_fpath,
                         get_entity_extractor_sorted_fpath)

def sort_entity_extractor(current_dir, concerned_date):
    ofpath = get_entity_extractor_fpath(current_dir, concerned_date)
    wfpath = get_entity_extractor_sorted_fpath(current_dir, concerned_date)
    sort_datetime(ofpath, wfpath)
    
def get_date_time(date):
    try:
        date_time = datetime.datetime.strptime(date, '%Y.%m.%d %H:%M:%S')
    except:
        date_time = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M')
    return date_time

def sort_datetime(fname, new_fname):
    new_data = []
    with open(fname) as f:
        for line in f:
            splitted = line.strip("\n").split("|")
            date = splitted[1]

            date_time = get_date_time(date)

            new_data.append((date_time, line))

    new_data.sort(key=lambda k: k[0], reverse=True)
#     print new_data

    with open(new_fname, "w") as wf:
        for date_time, new_line in new_data:
            wf.write(new_line)

#===============================================================================
# 对counter_collector出来的数据进行排序，词频最高的entity出现在第一行
#===============================================================================

def sort_counter(fname, new_fname):
    with open(new_fname, "w") as wf:
        name_counts = []
        with open(fname) as f:
            for line in f:
                splitted = line.split("::")
                name = splitted[0]
                count = splitted[1]
                name_counts.append([name, count])

        sorted_name_counts = sorted(name_counts, key=lambda k: k[1], reverse=True)
        for name, count in sorted_name_counts:
            wf.write('::'.join([name, count]))

#===============================================================================
# 处理编码问题
#===============================================================================

def transform_codec(fname, fname_after_transformed):
    with open(fname_after_transformed, "w") as wf:
        with open(fname) as f:
            for line in f:
                splitted = line.split("::")
                name = splitted[0]
                count = splitted[1]
                name = name.decode('gbk').encode('utf-8')
                wf.write("::".join([name, count]))

if __name__ == "__main__":
    pass
    # counter大小排序 & 编码问题
#     fname = "../io/counters/companies/companies_20140106090000_mon.txt"
#     fname_after_codec = "../io/counters/companies/companies_20140106090000_mon_codec.txt"
#     fname_after_sorted_and_codec = "../io/counters/companies/companies_20140106090000_mon_codec_sorted.txt"
#     transform_codec(fname, fname_after_codec)
#
#     sort_counter(fname_after_codec, fname_after_sorted_and_codec)
