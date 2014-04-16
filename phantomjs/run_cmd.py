#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: run_cmd.py
Description: this program offers recipes to run windows command line in python.
Creation: 2013-11-8
Revision: 2013-11-8
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

import subprocess
import pdb
from bs4 import BeautifulSoup as BS

import os
import sys
basepath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(basepath, "..")))

from timer import Timer

#===============================================================================
# The main objective is to accomplish:
# I could run "phantomjs rendering.js http://www.sse.com.cn/assortment/stock/list/stockdetails/company/index.shtml?COMPANY_CODE=600000".
# I wanna do an iteration over hundreds of URLs to get web pages after rendering for future analysis.
#===============================================================================

#===============================================================================
# simple examples
#===============================================================================

# subprocess.call('dir', shell=True)
# subprocess.call('exit', shell=True)

#===============================================================================
# Complicated examples:
# 1. args could be a string, or a sequence.
# 2. call & Popen
#===============================================================================

# subprocess.call(['phantomjs', "simple_rendering.js"], shell=True)
# subprocess.Popen(['phantomjs', "simple_rendering.js"], shell=True)

#===============================================================================
# Both of the following formats of running the same commands are available.
# ATTENTION: If missing 'stdout=subprocess.PIPE', the output "result" is NoneType.
#===============================================================================

# p = subprocess.Popen("phantomjs rendering.js http://www.yahoo.com/")  # str format
# p = subprocess.Popen(['phantomjs', "rendering.js", "https://appexchange.salesforce.com/listingDetail?listingId=a0N3000000266tNEAQ"], stdout=subprocess.PIPE)  # sequence format
# result = p.communicate()[0]
# print result
# print "detailsTabComponent:website" in result
# 
# soup = BS(result)
#     
# for each in soup.find_all('a'):
#     print each
#     try:
#         if each.id == "listingDetailPage:AppExchangeLayout:listingDetailForm:listingDetailDetailsTab:detailsTabComponent:website":
#             print each
#     except:
#         pass
# pdb.set_trace()

#===============================================================================
# Crawl the screen shots of webpages (批量)
# 1. 可能的错误：
#         TypeError: 'null' is not an object (evaluating '$('#slideshowHolder').jqFancyTransitions')

#           http://www.11antsanalytics.com/:288
#         ReferenceError: Can't find variable: __sfga

#           http://www.11antsanalytics.com/:327
# 2. 批量地跑10个，测试运行时间及可能出现的错误

#===============================================================================

# with open("../io/3k_company_websites_and_domains.txt") as f:
#     for i, line in enumerate(f):
#         if 20 > i > 9:
#             company_website, company_domain = line.strip().split("\t")
#             print company_website, company_domain
#             try:
#                 p = subprocess.Popen("phantomjs screen_capture.js '%s' '%s.png'" % (company_website, company_domain))
#             except:
#                 pass

#===============================================================================
# 单个网页生成截图
#===============================================================================

p = subprocess.Popen("phantomjs screen_capture.js 'http://www.3glp.com' '3glp.com.v2.png'")

#===============================================================================
# 通过wget获取网页html
#===============================================================================

# p = subprocess.Popen(["wget", "https://appexchange.salesforce.com/listingDetail?listingId=a0N30000004cvIeEAI"])
