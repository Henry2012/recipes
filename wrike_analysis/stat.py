#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: news_stat.stat.py
Description: this program
Creation: 2013-11-26
Revision: 2013-11-26
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

import datetime
import pdb
import json
from pprint import pprint
from collections import defaultdict

#===============================================================================
# 统计出每个域名下的新闻数量
#===============================================================================

with open("../io/salesforce_domains_v2.txt") as f1:
    domains = [line.strip() for line in f1.readlines()]
 
stat = {}
for domain in domains:
    stat[domain] = 0

with open("../io/news_filterd_20131210.json") as f:
    for line in f:
        record = json.loads(line.strip())
        url = record['url']
        domain = record['domain']
#         date = record['date']
#         name = record['name']
         
        stat[domain] += 1
 
with open('../io/stat_v4.txt', 'w') as wf:
    for k, v in stat.iteritems():
        wf.write("%s\t%s\n" % (k, v))

#===============================================================================
# 统计：
# 1. 晚于20110101的新闻
# 2. 没有时间的新闻
#===============================================================================

# count_of_recent_news = 0
# count_of_no_datetime_news = 0
# with open("../io/news_urls.json") as f:
#     for line in f:
#         record = json.loads(line.strip())
#         url = record['url']
#         domain = record['domain']
#         name = record['name']
#         
#         #===============================================================================
#         # unicode:
#         # 1. "2007-2-28"
#         # 2. "No-Date"
#         #===============================================================================
#         date = record['date']
#         if date == u"No-Date":
#             count_of_no_datetime_news += 1
#         else:
#             date_time = datetime.datetime.strptime(date, '%Y-%m-%d')
#             if date_time > datetime.datetime(2011, 1, 1):
#                 count_of_recent_news += 1
#         
# print count_of_recent_news
# print count_of_no_datetime_news

#===============================================================================
# 获得domain为socialmediagroup.com的所有链接
#===============================================================================
# urls = []
# with open("../io/socialmediagroup_hrefs.txt", 'w') as wf:
#     with open("../io/news_urls.json") as f:
#         for line in f:
#             record = json.loads(line.strip())
#             url = record['url']
#             domain = record['domain']
#             name = record['name']
#             type = record['type']
#             
#             if domain == "socialmediagroup.com":
#                 urls.append(url)
#                 wf.write(url + '\n')

#===============================================================================
# 分析页面http://socialmediagroup.com/2013/10/28/teched-las-vegas-what-i-learned-what-i-saw/
# 哪些被Hua的程序囊括，哪些被Hua的程序抛弃
#===============================================================================

# from pprint import pprint
# with open("../io/socialmediagroup_hrefs.txt") as f1:
#     all_urls = [line.strip() for line in f1]
#     
# with open("../io/hrefs_in_one_link_v1.txt") as f2:
#     hrefs = [line.strip() for line in f2]
#     
# print "http://diginomica.com/2013/08/30/sap-ui-overhaul-sam-yen/" in hrefs
# print "http://diginomica.com/2013/08/30/sap-ui-overhaul-sam-yen/" in all_urls
# 
# included = set(all_urls).intersection(set(hrefs))
# excluded = set(hrefs) - included
# 
# pprint(included)
# pdb.set_trace()
