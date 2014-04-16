#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: .py
Description: this program
Creation: 2014-2-17
Revision: 2014-2-17
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

import os
import pdb
import re
import sys
basepath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(basepath, "..")))

from file_names import (stock_quote_fname,
                        product_release_fname,
                        non_product_release_fname,
                        colon_with_one_quote_without_zhengquan_before_colon_without_hyphen_fname,
                        colon_with_one_quote_without_zhengquan_after_colon_without_hyphen_fname,
                        colon_with_one_quote_without_zhengquan_after_colon_revised_without_hyphen_fname,
                        colon_with_one_quote_without_zhengquan_before_colon_revised_without_hyphen_fname)
from preprocess_util import (replace_special_characters_before_seg,
                             revise_titles_with_quote_name_after_colon,
                             revise_titles_with_quote_name_before_colon)
from topic_extractor_util import (get_event_from_one_quote,
                                  get_event_from_more_quotes)
from util import (PRODUCT_RELEASE_KW,
                  get_stock_quotes)

#===============================================================================
# Get all stock quotes
#===============================================================================

STOCK_QUOTES = get_stock_quotes(stock_quote_fname)
    
#===============================================================================
# 预处理：
#     1. 特殊符号的替换（书名号，中文双引号，中文单引号，全角空格）
#     2. 去除含有"发布会"的记录
#     3. 对两种不同情形再调用已经有的函数（包含了第一步骤）
#===============================================================================

# revise_titles_with_quote_name_after_colon(colon_with_one_quote_without_zhengquan_after_colon_without_hyphen_fname,
#                                           colon_with_one_quote_without_zhengquan_after_colon_revised_without_hyphen_fname)
#  
# revise_titles_with_quote_name_before_colon(colon_with_one_quote_without_zhengquan_before_colon_without_hyphen_fname,
#                                            colon_with_one_quote_without_zhengquan_before_colon_revised_without_hyphen_fname)

#===============================================================================
# topic extractor
#===============================================================================

one_quote_fnames = (colon_with_one_quote_without_zhengquan_after_colon_revised_without_hyphen_fname,
                    colon_with_one_quote_without_zhengquan_before_colon_revised_without_hyphen_fname)
 
# print "# of keywords: ", len(PRODUCT_RELEASE_KW)
# count = 0
# for fname in one_quote_fnames:
#     count += get_event_from_one_quote(fname,
#                                   PRODUCT_RELEASE_KW,
#                                   product_release_fname,
#                                   non_product_release_fname)
#  
# print count

# pdb.set_trace()

#===============================================================================
# Some utilies
#===============================================================================

on_root_pattern = re.compile(r'root\(ROOT\-[0-9]+, (发布|推出)\-[0-9]+\)')

on_product_release_pattern = re.compile(r'dobj\((发布|推出)\-[0-9]+, (新品|产品|样机)\-[0-9]+?\)')
off_product_release_pattern = re.compile(r'dobj\((发布|推出)\-[0-9]+, (方案|草案|报告|报告书|公告|股价|计划|快报|利好|预案|修订稿|中报|报|季报|优先股|商标|激励|未定|澄清)\-[0-9]+?\)')

on_topic_pattern = re.compile(r'dobj\((发布|推出)\-[0-9]+, (.*?)\-[0-9]+\)')

(fname,
 on_product_release_fname,
 off_product_release_fname,
 all_else_fname) = ("../io/test_v2/product_release_v4_seg_dep.txt",
                    "../io/test_v2/on_product_release_v4.txt",
                    '../io/test_v2/off_product_release_v4.txt',
                    '../io/test_v2/all_else_within_product_release_v4.txt')

(on_topic_tier_2_fname,
 off_topic_tier_2_fname,
 all_else_tier_2_fname,
 on_topic_tier_3_fname,
 off_topic_tier_3_fname,
 all_else_tier_3_fname) = ('../io/test_v2/on_topic_tier_2_v4.txt',
                           '../io/test_v2/off_topic_tier_2_v4.txt',
                           '../io/test_v2/all_else_tier_2_v4.txt',
                           '../io/test_v2/on_topic_tier_3_v4.txt',
                           '../io/test_v2/off_topic_tier_3_v4.txt',
                           '../io/test_v2/all_else_tier_3_v4.txt',)

#===============================================================================
# 第一层次
#     1. white list
#     2. black list
#     3. all else
#===============================================================================

# with open(fname) as f:
#     with open(on_product_release_fname, 'w') as wf1:
#         with open(off_product_release_fname, 'w') as wf2:
#             with open(all_else_fname, 'w') as wf3:
#                 for line in f:
#                     dep = line.strip().split('\t')[0]
#                     flag = False
#                      
#                     if re.search(on_root_pattern, dep):
#                         if re.search(on_product_release_pattern, dep):
#                             wf1.write(line)
#                         elif re.search(off_product_release_pattern, dep):
#                             wf2.write(line)
#                         flag = True
#                      
#                     if not flag:
#                         wf3.write(line)

# pdb.set_trace()

#===============================================================================
# 第二层次（对第一层的all else）
#     1. on
#     2. off
#===============================================================================

# with open(all_else_fname) as f:
#     with open(on_topic_tier_2_fname, 'w') as wf1:
#         with open(off_topic_tier_2_fname, 'w') as wf2:
#             with open(all_else_tier_2_fname, 'w') as wf3:
#                 for line in f:
#                     dep, id, title = line.strip().split('\t')[:3]
#                     
#                     if re.search(off_product_release_pattern, dep):
#                         wf2.write(line)
#                     elif re.search(on_product_release_pattern, dep):
#                         wf1.write(line)
#                     else:
#                         wf3.write(line)

# pdb.set_trace()

#===============================================================================
# 第三层次（对第二层次的all else）
    
#===============================================================================

on_pattern_tier_3 = re.compile(r'.+\((发布|推出)\-[0-9]+, (新品|产品|样机)\-[0-9]+?\)')
on_pattern_tier_3_v2 = re.compile(r'.+\((新品|产品|样机)\-[0-9]+?, (发布|推出)\-[0-9]+\)')
off_pattern_tier_3 = re.compile(r'.+\((发布|推出)\-[0-9]+, (方案|草案|报告|报告书|公告|股价|计划|快报|利好|预案|修订稿|中报|报|季报|优先股|商标|激励|未定|澄清)\-[0-9]+?\)')
off_pattern_tier_3_v2 = re.compile(r'.+\((方案|草案|报告|报告书|公告|股价|计划|快报|利好|预案|修订稿|中报|报|季报|优先股|商标|激励|未定|澄清)\-[0-9]+?, (发布|推出)\-[0-9]+\)')

with open(all_else_tier_2_fname) as f:
    with open(on_topic_tier_3_fname, 'w') as wf1:
        with open(off_topic_tier_3_fname, 'w') as wf2:
            with open(all_else_tier_3_fname, 'w') as wf3:
                for line in f:
                    dep, id, title = line.strip().split('\t')[:3]
                     
                    if (re.search(off_pattern_tier_3, dep) or
                        re.search(off_pattern_tier_3_v2, dep) or
                        '发布会' in title):
                        wf2.write(line)
                    elif (re.search(on_pattern_tier_3, dep) or
                          re.search(on_pattern_tier_3_v2, dep)):
                        wf1.write(line)
                    else:
                        wf3.write(line)

