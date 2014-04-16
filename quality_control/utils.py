#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
Creation: 2014-1-3
Revision: 2014-1-3
"""

import os
import datetime

EMPTY_VALUE_MAPPING = {'str': "",
                       'list': [],
                       'dict': {},
                       'unicode': u''}

def get_current_time(flag="long"):
    # flag设置返回字符串是长字符串，还是短字符串
    if flag == "short":
        today_dtime = datetime.date.today()
        today_str = today_dtime.strftime('%Y%m%d')
    elif flag == "long":
        today_dtime = datetime.datetime.today()
        today_str = today_dtime.strftime('%Y%m%d%H%M')
    return today_str

def make_dirs(io_fpath, current_time, db_name, col_name):
    col_name = "_".join([col_name, current_time])
    col_fpath = os.path.join(io_fpath, db_name, col_name)
    
    # 判断目录col_fpath是否存在
    # 如果不存在，则创建目录
    # 最后返回col_fpath
    if not os.path.exists(col_fpath):
        os.makedirs(col_fpath)

    return os.path.realpath(col_fpath)

def get_angellist_keys(fname):
    angellist_keys = []
    with open(fname) as f:
        for line in f:
            #print line.strip()
            angellist_keys.append(line.strip())
    return angellist_keys

if __name__ == "__main__":
    
    #fname = "../io/angellist_comp_keys.txt"
    fname = "../io/crunchbase_people_keys.txt"
    print get_angellist_keys(fname)
    
    io_fpath, current_time, db_name, col_name = ('../io/test',
                                                 '20140120',
                                                 'es',
                                                 'zoominfo')
    print make_dirs(io_fpath, current_time, db_name, col_name)
    
    current_time = get_current_time()
    print current_time