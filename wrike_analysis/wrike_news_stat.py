#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: news_stat.wrike_news_stat.py
Description: this program gives the STAT for Wrike.
Creation: 2014-1-3
Revision: 2014-1-3
"""

import pymongo
from db_cfg import wrike_uri
from collections import defaultdict

import os
import sys
basepath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(basepath, "..")))

from timer import Timer
from send_gmail import send_gmail
from page_types import PAGE_TYPES

#===============================================================================
# Create connection to MongoDB
#===============================================================================

client = pymongo.MongoClient(wrike_uri)
db = client['wrike']
# col_name = "news"
col_name = "webpage"
col = db[col_name]

#===============================================================================
# Create STAT
#===============================================================================

domains = defaultdict(lambda: [0] * 27)

# 简单地统计domain出现的次数
# with Timer() as t:
#     for each in col.find({}):
#         domain = each['domain']
#         if domain:
#             domains[domain] += 1
#         else:
#             print domain
# print "The creation of STAT costs: ", t.interval

# 深入地统计不同页面类型的数量
with Timer() as t:
    for each in col.find({}):
        domain = each['domain']
        page_type = each['pagetype']
        type_id = PAGE_TYPES.index(page_type)
        
        if domain:
            domains[domain][0] += 1
            domains[domain][type_id + 1] += 1
print "The creation of STAT costs: ", t.interval

# sort the result based on freq
with Timer() as t:
    sorted_domains = sorted(domains.items(), key=lambda k: k[1][0], reverse=True)
print "Sorting STAT costs: ", t.interval

# save the result
with Timer() as t:
    with open("../io/wrike_webpage_stat.txt", "w") as wf:
        for (domain, count_list) in sorted_domains:
            count_str = "\t".join(str(each) for each in count_list)
            wf.write("\t".join([domain, count_str]) + "\n")
print "Writing to a text file costs: ", t.interval

send_gmail(gmail_user='hendyhqq',
           passwd="",
           recipient='815515379@qq.com',
           subject='Wrike News Stat',
           body='Done')

