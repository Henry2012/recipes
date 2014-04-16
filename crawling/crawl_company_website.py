#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: crawling.crawl_company_website.py
Description: this program
Creation: 2013-11-28
Revision: 2013-11-28
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

from bs4 import BeautifulSoup as BS
from recipes import get_html

url = "https://appexchange.salesforce.com/listingDetail?listingId=a0N30000001grN8EAI"
html = get_html(url)
with open("../io/sample_v2.txt", 'w') as wf:
    wf.write(html)
    
# soup = BS(html)
#     
# for each in soup.find_all('a'):
#     print each
#     try:
#         if each.id == "listingDetailPage:AppExchangeLayout:listingDetailForm:listingDetailDetailsTab:detailsTabComponent:website":
#             print each
#     except:
#         pass
# 
# def wget(fname):
#     prefix = "https://appexchange.salesforce.com"
#     with open(fname) as f:
#         for line in f:
#             urls = prefix + line
    
    