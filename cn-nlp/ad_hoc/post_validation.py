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

import os
import sys
basepath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(basepath, "..")))

from file_names import (colon_with_one_quote_without_zhengquan_before_colon_without_hyphen_fname,
                        colon_with_one_quote_without_zhengquan_after_colon_without_hyphen_fname,)

after_fname = colon_with_one_quote_without_zhengquan_after_colon_without_hyphen_fname
before_fname = colon_with_one_quote_without_zhengquan_before_colon_without_hyphen_fname
old_after_fname = '../io/titles_contain_colon_with_one_quote_without_zhengquan_after_colon_processed_without_hyphen_v2_seg_modified.txt'
old_before_fname = '../io/titles_contain_colon_with_one_quote_without_zhengquan_before_colon_processed_without_hyphen_v2_seg_modified.txt'

#===============================================================================
# 
#===============================================================================

with open('../io/stock_gain_v3.txt') as f:
    with open(old_after_fname) as old_after:
        old_after = old_after.readlines()
        for each in old_after:
            print [each]
            raw_input()
                

        
#===============================================================================
# First phase test
#===============================================================================

stock_gain_titles = []
with open('../io/stock_gain_v3.txt') as f:
    with open('../io/stock_gain_v3_post_validated.txt', 'w') as wf:
        for line in f:
            words = []
            for each in line.strip().rstrip("。").split():
                if each == '，':
                    each = " "
                words.append(each)
            title = "".join(words)
            new_line = title + '\n'
            stock_gain_titles.append(title)
            wf.write(new_line)
#             raw_input()

# 491
print len(set(stock_gain_titles))

new_stock_gain_titles = []
with open('../io/test_v1/stock_gain.txt') as f2:
    for line in f2:
        title = line.strip().split('\t')[1]
        new_stock_gain_titles.append(title)

# 801
print len(set(new_stock_gain_titles))

count = 0
for each in stock_gain_titles:
    exists = False
    for new_each in new_stock_gain_titles:
        if each in new_each:
            exists = True
            break
    
    if not exists:
        count += 1
        print each

# 0
print count