#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: .py
Description: this program
Creation: 2014-2-14
Revision: 2014-2-14
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

from util import get_fnames

#===============================================================================
# 获取所有文件名-路径的映射字典
#===============================================================================

FNAMES = get_fnames()

#===============================================================================
# 获取股票名
#===============================================================================

stock_quote_fname = FNAMES['stock_quote_fname']

#===============================================================================
# 获取topic_classification
#===============================================================================

(stock_gain_fname,
 non_stock_gain_fname) = (FNAMES['stock_gain_fname'],
                          FNAMES['non_stock_gain_fname'])
 
(product_release_fname,
 non_product_release_fname) = (FNAMES['product_release_fname'],
                               FNAMES['non_product_release_fname'])
 
(acquisition_fname,
 non_acquisition_fname) = (FNAMES['acquisition_fname'],
                               FNAMES['non_acquisition_fname'])
 
(analyst_ratings_fname,
non_analyst_ratings_fname) = (FNAMES['analyst_ratings_fname'],
                              FNAMES['non_analyst_ratings_fname'])

#===============================================================================
# data division and data cleansing
#===============================================================================

# top level division
top_level_division_fnames = (raw_fname,
zero_quote_fname,
one_quote_fname,
more_quotes_fname) = (FNAMES[each] for each in['raw_fname',
                                                'zero_quote_fname',
                                                'one_quote_fname',
                                                'more_quotes_fname'])

# one_quote
one_quote_fnames = ['one_quote_with_colon_fname',
'one_quote_with_colon_with_zhengquan_fname',
'one_quote_with_colon_with_zhengquan_before_colon_fname',
'one_quote_with_colon_with_zhengquan_before_colon_with_hyphen_fname',
'one_quote_with_colon_with_zhengquan_before_colon_without_hyphen_fname',
'one_quote_with_colon_with_zhengquan_after_colon_fname',
'one_quote_with_colon_with_zhengquan_after_colon_with_hyphen_fname',
'one_quote_with_colon_with_zhengquan_after_colon_without_hyphen_fname',
'one_quote_with_colon_without_zhengquan_fname',
'one_quote_with_colon_without_zhengquan_before_colon_fname',
'one_quote_with_colon_without_zhengquan_before_colon_with_hyphen_fname',
'one_quote_with_colon_without_zhengquan_before_colon_with_hyphen_between_hyphen_and_colon_fname',
'one_quote_with_colon_without_zhengquan_before_colon_with_hyphen_not_between_hyphen_and_colon_fname',
'one_quote_with_colon_without_zhengquan_before_colon_without_hyphen_fname',
'one_quote_with_colon_without_zhengquan_after_colon_fname',
'one_quote_with_colon_without_zhengquan_after_colon_with_hyphen_fname',
'one_quote_with_colon_without_zhengquan_after_colon_without_hyphen_fname']

(one_quote_with_colon_fname,
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
one_quote_with_colon_without_zhengquan_after_colon_without_hyphen_fname) = (FNAMES[each] for each in one_quote_fnames)


(colon_with_more_quotes_fname,
colon_with_more_quotes_with_hyphen_fname,
colon_with_more_quotes_without_hyphen_fname,
colon_with_more_quotes_without_hyphen_with_zhengquan_and_colon_fname,
colon_with_more_quotes_without_hyphen_without_zhengquan_and_colon_fname,) = (
    FNAMES[each] for each in ['colon_with_more_quotes_fname',
                              'colon_with_more_quotes_with_hyphen_fname',
                              'colon_with_more_quotes_without_hyphen_fname',
                              'colon_with_more_quotes_without_hyphen_with_zhengquan_and_colon_fname',
                              'colon_with_more_quotes_without_hyphen_without_zhengquan_and_colon_fname'])

# for word segmentation, PoS, and dependencies
(one_quote_with_colon_without_zhengquan_after_colon_revised_without_hyphen_fname,
 one_quote_with_colon_without_zhengquan_before_colon_revised_without_hyphen_fname) = (FNAMES[each] for each in ('one_quote_with_colon_without_zhengquan_after_colon_revised_without_hyphen_fname',
                                                                                                                'one_quote_with_colon_without_zhengquan_before_colon_revised_without_hyphen_fname'))

# event counter
init_event_id_fname = FNAMES['init_event_id_fname']

# event distinction pkl files
stock_gain_event_distinction_fname = FNAMES['stock_gain_event_distinction_fname'][:-4]
analyst_ratings_event_distinction_fname = FNAMES['analyst_ratings_event_distinction_fname'][:-4]

(one_quote_with_colon_without_zhengquan_before_colon_with_hyphen_between_hyphen_and_colon_fname,
 one_quote_with_colon_without_zhengquan_before_colon_with_hyphen_not_between_hyphen_and_colon_fname) = (FNAMES[each] for each in ('one_quote_with_colon_without_zhengquan_before_colon_with_hyphen_between_hyphen_and_colon_fname',
                                                                                                                                  'one_quote_with_colon_without_zhengquan_before_colon_with_hyphen_not_between_hyphen_and_colon_fname'))
(colon_with_more_quotes_with_hyphen_with_all_quotes_in_front_fname,
 colon_with_more_quotes_with_hyphen_without_all_quotes_in_front_fname) = (FNAMES[each] for each in ('colon_with_more_quotes_with_hyphen_with_all_quotes_in_front_fname',
                                                                                                    'colon_with_more_quotes_with_hyphen_without_all_quotes_in_front_fname'))