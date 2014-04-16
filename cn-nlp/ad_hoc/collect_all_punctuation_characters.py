#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: .py
Description: this program
Creation: 2014-2-20
Revision: 2014-2-20
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

import pdb
import re
from pprint import pprint

def get_punc_characters(sent):
    characters = set()
    for each in re.findall(ur'([^\u4e00-\u9fa5\w])', unicode(sent, 'utf8')):
        characters.add(each)
    return characters

with open('../io/test_v2/event_alpha_for_prod_20140208.txt') as f:
    all = set()
    for i, line in enumerate(f):
#         if i > 100000:
#             break
        splitted_line = line.strip().split('\t')
        title = splitted_line[1]
        all.update(get_punc_characters(title))

all_in_list = list(all)
print u'0' in all
print len(all_in_list)
for each in all_in_list:
    print each
pdb.set_trace()