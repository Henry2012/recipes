#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: crawling.crawl_cikuapi.py
Description: this program crawls words in http://cikuapi.com/.
Creation: 2013-11-12
Revision: 2013-11-12
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

#===============================================================================
# Main objective:
# 1. 利用http://cikuapi.com/爬取金融相关的词汇
#===============================================================================

# import pdb
import re
import urllib
from bs4 import BeautifulSoup as BS
from recipes import get_html

root = "证券"
url = "http://cikuapi.com/index.php?content=" + urllib.quote(root)

text = get_html(url)
# print dir(text)
# print type(text)
# print "info: ", text.info()
# print "msg: ", text.msg
# print "read: ", text.read(), type(text.read())
soup = BS(text)
# print soup.prettify()

#===============================================================================
# Extract degrees of relevance level
#===============================================================================
def get_degrees(text):
    degrees = []
    pattern = re.compile(r"([01].[0-9]{6})")
    for match in re.finditer(pattern, text):
        degrees.append(match.group(1))
        
    return degrees

#===============================================================================
# BeautifulSoup:查看网页编码
#===============================================================================
# soup = BS(text, from_encoding='utf-8')

# print soup.original_encoding
# print soup.declared_html_encoding
# print soup.from_encoding

#===============================================================================
# 抓取相关词
#===============================================================================
def get_related_words(soup):
    with open('../io/_temp.txt', 'a') as wf:
        for each in soup.find_all('font'):
            related = each.text.encode('utf-8')
            print related
            wf.write(related + '\n')
        wf.write('\n')

if __name__ == "__main__":
    print get_degrees(text)
#     get_related_words(soup)
    pass
