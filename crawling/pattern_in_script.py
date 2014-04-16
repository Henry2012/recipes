#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: crawling.pattern_in_script.py
Description: this program
Creation: 2013-11-27
Revision: 2013-11-27
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

import json
from lxml import html
from lxml.html import fromstring
from lxml import etree
from pprint import pprint

# srcs_in_test = []
# with open("../io/test_100.json") as f:
#     for line in f:
#         d = json.loads(line.strip())
#         html_text = d['html']
#         if html_text:
#             try:
#                 tree = html.fromstring(html_text)
#                 srcs = tree.xpath("//script/@src")
#                 if srcs:
#                     srcs_in_test.extend(srcs)
#             except:
#                 pass
#  
# # with open("../io/srcs_in_test.txt", 'w') as wf:
# #     for each in srcs_in_test:
# #         wf.write(each + '\n')
# 
# srcs_in_patterns = []
# with open("../io/js_patterns.txt", 'w') as wf:
#     with open("../io/patterns.txt") as f:
#         for each in f:
#             if each.strip().endswith(".js"):
#                 srcs_in_patterns.append(each.strip())
#                 wf.write(each)
# 
# common_srcs = []
# # common_srcs = set(srcs_in_test).intersection(set(srcs_in_patterns))
# 
# for src_in_p in srcs_in_patterns:
#     for src_in_t in srcs_in_test:
#         if src_in_p in src_in_t:
#             common_srcs.append(src_in_p)
#             break
# 
# print len(common_srcs)
# 
# with open("../io/common_srcs.txt", 'w') as wf:
#     for each in common_srcs:
#         wf.write(each+"\n")
#         
# with open("../io/rest_srcs.txt", 'w') as wf:
#     for each in set(srcs_in_patterns) - set(common_srcs):
#         wf.write(each+"\n")
    
#===============================================================================
# Find patterns ending with ".js" which haven't occurred in common_srcs
#===============================================================================

# patterns = []
# with open("../io/rest_srcs.txt") as f:
#     for line in f:
#         patterns.append(line.strip())
# 
# matching_patterns = []
# with open("../io/test_100.json") as f:
#     for i, line in enumerate(f):
#         d = json.loads(line.strip())
#         html_text = d['html']
#         if html_text:
#             for pattern in patterns:
#                 if pattern in html_text:
#                     matching_patterns.append(pattern)
#                     print
#                     print i, pattern
#                     raw_input()
#                     
# print len(matching_patterns)
# 
# with open("../io/matching_patterns_from_rest.txt", 'w') as wf:
#     for each in matching_patterns:
#         wf.write(each+"\n")

#===============================================================================
# print prettify
#===============================================================================

from bs4 import BeautifulSoup as BS

with open('../io/test_1.json') as f:
    for line in f:
        html = line.strip()
        soup = BS(html)
        print soup.prettify()