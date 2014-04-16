#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: .py
Description: this program
Creation: 2014-3-17
Revision: 2014-3-17
"""

import os
import datetime
import pdb
import sys
basepath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(basepath, "..")))

import codecs
import re
from commonregex import CommonRegex
from recipe import (get_title_seg_splitted,
                    get_fpath_based_on_flag)
from util import (contains_media_date_in_title)

#===============================================================================
# 收购事件：
# 1. 首先，查找“收购”是否出现在title中--->acqu_shougou.txt
# 2. 接着，查找“并购”--->acqu_binggou.txt
# 3. 最后，剩下的--->acqu_else.txt
#===============================================================================

# event_type = 'acqu
# flags = ('shougou', 'binggou', 'else')
# f1, f2, f3 = (get_fpath_based_on_flag(flag, event_type) for flag in flags)
# of1 = open(f1,'w')
# of2 = open(f2,'w')
# of3 = open(f3,'w')
# with open('../io/test_v3/stock_news_for_acqu.txt') as f:
#     for line in f:
#         id, title, title_pos = line.strip().split('\t')
#         title_pos_splitted = title_pos.split(' ')
#         title_seg_splitted = get_title_seg_splitted(title_pos_splitted)
#         
#         if '收购' in title:
#             of1.write(line)
#         elif '并购' in title:
#             of2.write(line)
#         else:
#             of3.write(line)
            
#===============================================================================
# 百分号事件（业绩|净利|盈利|利润|营收|收入）
#===============================================================================

# event_type = 'percentage'
# flags = ('yeji_n_jingli', 'else')
# f1, f2 = (get_fpath_based_on_flag(flag, event_type) for flag in flags)
# with open('../io/test_v3/stock_news_for_percentage.txt') as f:
#     with open(f1, 'w') as wf1:
#         with open(f2, 'w') as wf2:
#             for line in f:
#                 title = line.strip()
#                 if re.search(r'业绩|净利|盈利|利润|营收|收入', title):
#                     wf1.write(line)
#                 else:
#                     wf2.write(line)
                    
#===============================================================================
# 全量数据中抽取earnings事件
#===============================================================================

event_type = 'earnings'
pattern = ur'业绩|净利|盈利|利润|营收|收入'
flags = ('on', 'off')
f1, f2 = (get_fpath_based_on_flag(flag, event_type) for flag in flags)
with codecs.open('../io/test_v3/with_at_least_1_quotes.txt', 'r', 'utf-8') as f:
    with codecs.open(f1, 'w', 'utf-8') as wf1:
        with codecs.open(f2, 'w', 'utf-8') as wf2:
            for line in f:
                id, title, quotes, media_date = line.strip().split("\t")
                if re.search(pattern, title):
                    wf1.write(line)
                else:
                    wf2.write(line)

#===============================================================================
# 找到ratings相关的新闻
#===============================================================================

# pattern1 = ur'[0-9\.]+.{0,2}-+[0-9\.]+.{0,2}'
# pattern2 = ur'业绩|净利|盈利|利润|营收|收入'
# 
# with codecs.open('../io/test_v3/test.txt', 'r', 'utf-8') as f:
#     with codecs.open('../io/test_v3/test_on_ratings.txt', 'w', 'utf-8') as wf1:
#         with codecs.open('../io/test_v3/test_off_ratings.txt', 'w', 'utf-8') as wf2:
#             for line in f:
#                 title, quotes = line.strip().split('\t')
#                 
#                 on_topic_flag = True
#                 if re.search(pattern2, title):
#                     on_topic_flag = False
#                 elif re.search(pattern1, title):
#                     on_topic_flag = False
#                     
#                 if on_topic_flag:
#                     wf1.write(line)
#                 else:
#                     wf2.write(line)

#===============================================================================
# 测试
#===============================================================================

# pattern = ur'[0-9\.]+.{0,2}-+[0-9\.]+.{0,2}'
# with codecs.open('../io/test_v3/contains_hyphen_with_at_least_1_quotes_contains_none.txt', 'r', 'utf-8') as f:
#     with codecs.open('../io/test_v3/contains_hyphen_with_at_least_1_quotes_contains_none_on.txt', 'w', 'utf-8') as wf1:
#         with codecs.open('../io/test_v3/contains_hyphen_with_at_least_1_quotes_contains_none_off.txt', 'w', 'utf-8') as wf2:
#             for line in f:
#                 id, title = line.strip().split('\t')
#                 if re.search(pattern, title):
#                     wf1.write(line)
#                 else:
#                     wf2.write(line)
                    
#===============================================================================
# 提取证券晨报的新闻
#===============================================================================

# with codecs.open('../io/test_v3/with_at_least_1_quotes.txt', 'r', 'utf-8') as f:
#     with codecs.open('../io/test_v3/with_at_least_1_quotes_on_chenbao.txt', 'w', 'utf-8') as wf1:
#         with codecs.open('../io/test_v3/with_at_least_1_quotes_off_chenbao.txt', 'w', 'utf-8') as wf2:
#             pattern = ur'[0-9\.]+.{0,2}-+[0-9\.]+.{0,2}'
#             for line in f:
#                 id, title, quotes, media_date = line.strip().split('\t')
#                  
#                 if not re.search(pattern, title):
#                     if "证券" in quotes:
#                         if contains_media_date_in_title(title, media_date):
#                             wf1.write(line)
#                         else:
#                             wf2.write(line)
                        
#===============================================================================
# 提取出所有含有“证券”的公司名
#    1. 总计14家公司名
#    2. company表中总计有18家含有“证券”的公司名
#===============================================================================

# companies = set()
# with codecs.open('../io/test_v3/with_at_least_1_quotes_contains_none_with_media_date_on_chenbao.txt', 'r', 'utf-8') as f:
#     pattern = ur'.{2}证券'
#     
#     for line in f:
#         id, title, media_date = line.strip().split('\t')
#         match = re.search(pattern, title)
#         if match:
#             companies.add(match.group())
#         else:
#             print title
# print len(companies)
# pdb.set_trace()

          
                
                 

