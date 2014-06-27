#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: crawling.recipes.py
Description: this program deals with web crawling.
Creation: 2013-11-8
Revision: 2013-11-8
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

import pdb
import re
import requests
import urllib2
import urllib
import urlparse
import sys
from lxml import html

reload(sys)
sys.setdefaultencoding('utf-8')

from bs4 import BeautifulSoup
#from lxml.html import fromstring

def get_html(url):
    #===============================================================================
    # 1. urllib2.urlopen(url).read()返回string格式的html
    # 2. 未经read()或者经过read()返回的值都可以作为BeautifulSoup的输入
    #===============================================================================
    response = urllib2.urlopen(url)
    html_src = response.read()
    response.close()
    return html_src

    #===============================================================================
    # 曾经在爬取中文页面时出现乱码，改用urllib2时OK了
    #===============================================================================
    #return requests.get(url, headers={"User-Agent": "Magic Browser"}).text

def get_page(url):
    #===============================================================================
    # 将字符串型的网页源代码转换成lxml可以识别的类
    #===============================================================================
    
    html_src = get_html(url)
    page = html.fromstring(html_src)
    return page

#===============================================================================
# URL中文编码
# 1. urllib.unquote
# 2. urlparse.unquote
# 3. urllib.quote
# 4. urllib.quote_plus
#     1. Spaces are encoded to +
#     2. + is encoded to %2B
#     3. % is encoded to %25
#===============================================================================

# print urllib.unquote("%E8%92%BC%E4%BA%95%E3%81%9D%E3%82%89")
# print [urlparse.unquote(urlparse.unquote("%2500%25c8%25c1%2500%25bf%25c2%2501%25b0%25b4%2503%259d%25cd%2502%25b4%25d6%2504%25b4%25a1"))]

# print urllib.quote_plus(urllib.quote_plus('Hello world!'))
# print urllib.quote('学大教育登陆')
# print urllib.unquote('%E5%AD%A6%E5%A4%A7%E6%95%99%E8%82%B2%E7%99%BB%E9%99%86')
print urllib.unquote('%E5%B0%8F%E9%B1%BC%E5%84%BF%E4%B8%8E%E8%8A%B1%E6%97%A0%E7%BC%BA%E7%94%B5%E8%A7%86%E5%89%A7').decode(encoding='utf8')
print urllib.unquote('1349,2865,1366,768')
raw_input()
#/qiso3/?if=pps_mobile&key=%E5%B0%8F%E9%B1%BC%E5%84%BF%E4%B8%8E%E8%8A%B1%E6%97%A0%E7%BC%BA%E7%94%B5%E8%A7%86%E5%89%A7&ctgname=&pageNum=1&pageSize=20
#===============================================================================
# 1.提取利用百度搜索使用的query（乱码格式）
# 2.将乱码转换成中文字符
# 【例】从URL:http://www.baidu.com/s?wd=%E6%9C%80%E6%96%B0%E7%94%B5%E5%BD%B1&ie=utf-8&tn=24008039_dg提取出“最新电影”
#===============================================================================

def get_search_query(url):
    pattern = r"wd=(.*?)&"
    match = re.search(pattern, url)
    #pdb.set_trace()
    if match:
        query = match.group(1)
        return urllib.unquote(query)
    #pdb.set_trace()

#===============================================================================
# 抓取特定部分的页面时，BeautifulSoup中最常用的命令莫过于find_all方法。
#===============================================================================

#===============================================================================
# 使用urlparse解析URL：
# scheme
# netloc
# path
# params
# query
# fragment
# username
# password
# hostname, '(netloc in lower case)'
# port
#===============================================================================
from urlparse import urlparse, parse_qsl

def parse_url(url):
    parsed = urlparse(url)
    print "Query: ", parsed.query
    print "Scheme: ", parsed.scheme
    print "Port: ", parsed.port
    print "Netloc: ", parsed.netloc
    
    # 解析以?开头的query strings成key-value对
    print "Query string: ", parse_qsl(parsed.query)
    
from referer_parser import Referer

def get_detailed_referer(referer_url):
#     referer_url = 'http://www.google.com/search?q=gateway+oracle+cards+denise+linn&hl=en&client=safari'
#     referer_url = "http://www.baidu.com/s?wd=python&rsv_bp=0&ch=&tn=baidu&bar=&rsv_spt=3&ie=utf-8&rsv_sug3=7&rsv_sug=0&rsv_sug4=1420&rsv_sug1=1&inputT=3105"
#     referer_url = "https://www.google.com.hk/search?q=python+%E8%A7%A3%E6%9E%90url&oq=python+%E8%A7%A3%E6%9E%90url&aqs=chrome..69i57j0l2j69i64.7609j0j7&sourceid=chrome&espv=210&es_sm=93&ie=UTF-8"

    r = Referer(referer_url)
    print(r.known)              # True
    print(r.referer)            # 'Google'
    print(r.medium)             # 'search'
    print(r.search_parameter)   # 'q'     
    print(r.search_term)        # 'gateway oracle cards denise linn'
    print(r.uri)      

if __name__ == "__main__":
    #===============================================================================
    # 获得baidu搜索关键词
    #===============================================================================
#     urls = ["http://www.baidu.com/s?wd=1%E5%8F%B7%E5%BA%97&rsv_spt=1&issp=1&rsv_bp=0&ie=utf-8&tn=baiduhome_pg&rsv_sug3=4&rsv_sug4=158&rsv_sug=1&rsv_sug1=3",
#             "http://www.baidu.com/s?wd=%E6%9C%80%E6%96%B0%E7%94%B5%E5%BD%B1&ie=utf-8&tn=24008039_dg",
#             "http://www.baidu.com/s?tn=24008039_dg&ie=utf-8&bs=%E6%9C%80%E6%96%B0%E7%94%B5%E5%BD%B1&f=3&rsv_bp=1&wd=%E6%9C%80%E6%96%B0%E7%94%B5%E5%BD%B1%E9%99%A2%E7%BA%BF&rsv_sug3=5&rsv_sug=0&rsv_sug1=5&rsv_sug4=70&oq=%E6%9C%80%E6%96%B0%E7%94%B5%E5%BD%B1%E5%8E%9F%E5%85%88&rsp=0&rsv_sug2=1&rsv_sug5=0&inputT=5936",
#             "http://www.baidu.com/s?wd=OLAY%E7%BE%8E%E8%82%8C%20%E5%B9%BF%E5%91%8A%E6%9B%B2&pn=50&tn=92182484_hao_pg&ie=utf-8"]
#     for url in urls:
#         print get_search_query(url)
    
    #===============================================================================
    # 获得该链接下的所有href
    #===============================================================================
    url = "http://socialmediagroup.com/2013/10/28/teched-las-vegas-what-i-learned-what-i-saw/"
#     url = "http://socialmediagroup.com/2008/04/28/social-media-press-releases-your-secret-weapon/"
    html_text = get_html(url)
    page = get_page(url)
#     doc = fromstring(html_text)
#     urls = doc.xpath('//a/@href')
#     with open("../io/hrefs_in_one_link_v1.txt", 'w') as wf:
#         for u in urls:
#             wf.write(u + '\n')
    pdb.set_trace()

    #===============================================================================
    # test whether a page is invalid
    #===============================================================================
#     try:
#         url = "http://www.spreems.com"
#         print get_html(url)
#     except urllib2.URLError:
#         print "Error"

    #===============================================================================
    # 解析URL
    #===============================================================================
#     urls = ["https://www.google.com.hk/search?q=python+%E8%A7%A3%E6%9E%90url&oq=python+%E8%A7%A3%E6%9E%90url&aqs=chrome..69i57j0l2j69i64.7609j0j7&sourceid=chrome&espv=210&es_sm=93&ie=UTF-8",
#            "http://product.auto.163.com/dealer/search/all_504_1684_0_%25E5%25A5%25A5%25E8%25BF%25AA_5_1.html"]
#      
#     for url in urls:
#         parse_url(url)
#         print "-" * 50
        
    #===============================================================================
    # extracting marketing attribution data (such as search terms) from referer URLs
    # 从URL中提取市场营销相关的数据（比如搜索关键字）
    #===============================================================================
#     with open("../io/url_snippet.txt") as f:
#         for line in f:
#             url = line.strip()
#             get_detailed_referer(url)
