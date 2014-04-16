#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: .py
Description: this program
Creation: 2014-2-13
Revision: 2014-2-13
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

import os
import sys
basepath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(basepath, "..")))

from pprint import pprint
from file_names import (one_quote_with_colon_fname,
                        one_quote_with_colon_with_zhengquan_fname,
                        one_quote_with_colon_with_zhengquan_before_colon_fname,
                        one_quote_with_colon_with_zhengquan_before_colon_with_hyphen_fname,
                        one_quote_with_colon_with_zhengquan_before_colon_without_hyphen_fname,
                        one_quote_with_colon_with_zhengquan_after_colon_fname,
                        one_quote_with_colon_with_zhengquan_after_colon_with_hyphen_fname,
                        one_quote_with_colon_with_zhengquan_after_colon_without_hyphen_fname,
                        one_quote_with_colon_without_zhengquan_fname,
                        one_quote_with_colon_without_zhengquan_before_colon_fname,
                        one_quote_with_colon_without_zhengquan_before_colon_with_hyphen_fname,
                        one_quote_with_colon_without_zhengquan_before_colon_with_hyphen_between_hyphen_and_colon_fname,
                        one_quote_with_colon_without_zhengquan_before_colon_with_hyphen_not_between_hyphen_and_colon_fname,
                        one_quote_with_colon_without_zhengquan_before_colon_without_hyphen_fname,
                        one_quote_with_colon_without_zhengquan_after_colon_fname,
                        one_quote_with_colon_without_zhengquan_after_colon_with_hyphen_fname,
                        one_quote_with_colon_without_zhengquan_after_colon_without_hyphen_fname)
from preprocess_util import (process_titles_concerning_signs,
                             process_titles_concerning_quotes,
                             process_titles_concerning_zhengquan,
                             process_titles_concerning_quote_and_colon_position,
                             process_titles_concerning_hyphen,
                             process_titles_concerning_zhengquan_and_colon,
                             revise_titles_with_quote_name_after_colon,
                             revise_titles_with_quote_name_before_colon,
                             process_titles_concerning_one_quote_and_hyphen_position,
                             process_titles_concerning_all_quotes_and_hyphen_position)
from util import (get_absolute_paths,
                  get_stock_quotes,
                  get_fnames)

#===============================================================================
# Get all file names
#===============================================================================

FNAMES = get_fnames()

#===============================================================================
# Get all stock quotes
#===============================================================================

stock_quote_fname = FNAMES['stock_quote_fname']
STOCK_QUOTES = get_stock_quotes(stock_quote_fname)

#===============================================================================
# process based on # of quotes
#===============================================================================

(raw_fname,
zero_quote_fname,
one_quote_fname,
more_quotes_fname) = (FNAMES['raw_fname'], FNAMES['zero_quote_fname'],
                      FNAMES['one_quote_fname'], FNAMES['more_quotes_fname'])
process_titles_concerning_signs(raw_fname,
                                zero_quote_fname,
                                one_quote_fname,
                                more_quotes_fname)

#===============================================================================
# process based on signs
#     1. colon
#     2. blank
#===============================================================================

colon_with_zero_quote_fname = FNAMES['colon_with_zero_quote_fname']
one_quote_with_colon_fname = FNAMES['one_quote_with_colon_fname']
colon_with_more_quotes_fname = FNAMES['colon_with_more_quotes_fname']
# process_titles_concerning_quotes(colon_fname, STOCK_QUOTES,
#                           colon_with_zero_quote_fname,
#                           one_quote_with_colon_fname,
#                           colon_with_more_quotes_fname)

#===============================================================================
# contains “证券” in quote names
#===============================================================================

(one_quote_with_colon_with_zhengquan_fname,
 one_quote_with_colon_without_zhengquan_fname) = (FNAMES['one_quote_with_colon_with_zhengquan_fname'],
                                                  FNAMES['one_quote_with_colon_without_zhengquan_fname'])

# process_titles_concerning_zhengquan(one_quote_with_colon_fname,
#                                     one_quote_with_colon_with_zhengquan_fname,
#                                     one_quote_with_colon_without_zhengquan_fname)

#===============================================================================
# 考虑股票名和冒号的位置关系
#===============================================================================

(one_quote_with_colon_with_zhengquan_fname,
 one_quote_with_colon_with_zhengquan_before_colon_fname,
 one_quote_with_colon_with_zhengquan_after_colon_fname,
 one_quote_with_colon_without_zhengquan_fname,
 one_quote_with_colon_without_zhengquan_before_colon_fname,
 one_quote_with_colon_without_zhengquan_after_colon_fname) = (
    FNAMES['one_quote_with_colon_with_zhengquan_fname'],
    FNAMES['one_quote_with_colon_with_zhengquan_before_colon_fname'],
    FNAMES['one_quote_with_colon_with_zhengquan_after_colon_fname'],
    FNAMES['one_quote_with_colon_without_zhengquan_fname'],
    FNAMES['one_quote_with_colon_without_zhengquan_before_colon_fname'],
    FNAMES['one_quote_with_colon_without_zhengquan_after_colon_fname'])
             
# process_titles_concerning_quote_and_colon_position(one_quote_with_colon_with_zhengquan_fname,
#                                                    one_quote_with_colon_with_zhengquan_before_colon_fname,
#                                                    one_quote_with_colon_with_zhengquan_after_colon_fname)
# process_titles_concerning_quote_and_colon_position(one_quote_with_colon_without_zhengquan_fname,
#                                                    one_quote_with_colon_without_zhengquan_before_colon_fname,
#                                                    one_quote_with_colon_without_zhengquan_after_colon_fname)

#===============================================================================
# contains hyphen pattern: ".+-.+："
#===============================================================================

hyphen_related = [(one_quote_with_colon_with_zhengquan_before_colon_fname,
  one_quote_with_colon_with_zhengquan_before_colon_with_hyphen_fname,
  one_quote_with_colon_with_zhengquan_before_colon_without_hyphen_fname),
 (one_quote_with_colon_with_zhengquan_after_colon_fname,
one_quote_with_colon_with_zhengquan_after_colon_with_hyphen_fname,
one_quote_with_colon_with_zhengquan_after_colon_without_hyphen_fname,),
 (one_quote_with_colon_without_zhengquan_before_colon_fname,
one_quote_with_colon_without_zhengquan_before_colon_with_hyphen_fname,
one_quote_with_colon_without_zhengquan_before_colon_without_hyphen_fname,),
 (one_quote_with_colon_without_zhengquan_after_colon_fname,
one_quote_with_colon_without_zhengquan_after_colon_with_hyphen_fname,
one_quote_with_colon_without_zhengquan_after_colon_without_hyphen_fname,)] = [(FNAMES[f1], FNAMES[f2], FNAMES[f3]) for (f1, f2, f3) in [
 ('one_quote_with_colon_with_zhengquan_before_colon_fname',
  'one_quote_with_colon_with_zhengquan_before_colon_with_hyphen_fname',
  'one_quote_with_colon_with_zhengquan_before_colon_without_hyphen_fname'),
 ('one_quote_with_colon_with_zhengquan_after_colon_fname',
  'one_quote_with_colon_with_zhengquan_after_colon_with_hyphen_fname',
  'one_quote_with_colon_with_zhengquan_after_colon_without_hyphen_fname'),
 ('one_quote_with_colon_without_zhengquan_before_colon_fname',
  'one_quote_with_colon_without_zhengquan_before_colon_with_hyphen_fname',
  'one_quote_with_colon_without_zhengquan_before_colon_without_hyphen_fname'),
 ('one_quote_with_colon_without_zhengquan_after_colon_fname',
  'one_quote_with_colon_without_zhengquan_after_colon_with_hyphen_fname',
  'one_quote_with_colon_without_zhengquan_after_colon_without_hyphen_fname')]]

# for each in hyphen_related:
#     process_titles_concerning_hyphen(*each)

# process_titles_concerning_hyphen(colon_with_more_quotes_fname,
#                         colon_with_more_quotes_with_hyphen_fname,
#                         colon_with_more_quotes_without_hyphen_fname)

#===============================================================================
# 确定"证券："是否在title里出现
#===============================================================================

# process_titles_concerning_zhengquan_and_colon(colon_with_more_quotes_without_hyphen_fname,
#                                               colon_with_more_quotes_without_hyphen_without_zhengquan_and_colon_fname,
#                                               colon_with_more_quotes_without_hyphen_with_zhengquan_and_colon_fname)

#===============================================================================
# for word segmentation, PoS, and Dependencies
#===============================================================================

revise_titles_with_quote_name_after_colon(one_quote_with_colon_without_zhengquan_after_colon_without_hyphen_fname,
                                          one_quote_with_colon_without_zhengquan_after_colon_revised_without_hyphen_fname)
revise_titles_with_quote_name_before_colon(one_quote_with_colon_without_zhengquan_before_colon_without_hyphen_fname,
                                           one_quote_with_colon_without_zhengquan_before_colon_revised_without_hyphen_fname)

#===============================================================================
# 对于只有一个公司名，并且满足：
#     1. 公司名中不包含“证券”
#     2. 公司名在第一个冒号之前
#     3. 包含连字符pattern
# 将满足以上的文件分成：
#     1. 唯一公司名出现在第一个连字符和冒号之间
#     2. all else
#===============================================================================

# process_titles_concerning_one_quote_and_hyphen_position(one_quote_with_colon_without_zhengquan_before_colon_with_hyphen_fname,
#                                                         one_quote_with_colon_without_zhengquan_before_colon_with_hyphen_between_hyphen_and_colon_fname,
#                                                         one_quote_with_colon_without_zhengquan_before_colon_with_hyphen_not_between_hyphen_and_colon_fname)

#===============================================================================
# 对于含有多个公司名，并且满足：
#     1. 含有连字符
# 提取出：
#     1. 公司名都在第一个冒号前面
#     2. all else
#===============================================================================

# process_titles_concerning_all_quotes_and_hyphen_position(colon_with_more_quotes_with_hyphen_fname,
#                                                          colon_with_more_quotes_with_hyphen_with_all_quotes_in_front_fname,
#                                                          colon_with_more_quotes_with_hyphen_without_all_quotes_in_front_fname)