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
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from bs4 import BeautifulSoup
#from lxml.html import fromstring

def get_html(url):
    #===============================================================================
    # 1. urllib2.urlopen(url).read()返回string格式的html
    # 2. 未经read()或者经过read()返回的值都可以作为BeautifulSoup的输入
    #===============================================================================
    return urllib2.urlopen(url).read()
    #return urllib2.urlopen(url)

    #return page = urllib2.urlopen(url)
    
    #===============================================================================
    # 曾经在爬取中文页面时出现乱码，改用urllib2时OK了
    #===============================================================================
    #return requests.get(url, headers={"User-Agent": "Magic Browser"}).text

#===============================================================================
# URL中文编码
# 1. urllib.unquote
# 2. urlparse.unquote
#===============================================================================

# print urllib.unquote("%E8%92%BC%E4%BA%95%E3%81%9D%E3%82%89")
# print urllib.quote("金融")
# print urllib.unquote("http://cikuapi.com/index.php?content=%E9%87%91%E8%9E%8D&bs=%E9%87%91%E8%9E%8D")
# print urllib.unquote("http://cikuapi.com/index.php?content=%E9%93%B6%E8%A1%8C")
# print urllib.quote("车")
# print urllib.quote("汽车")
# print urllib.unquote("%D4%D0%B8%BE%D7%B0%C7%EF%D7%B0").decode('gb2312')
# print urllib.unquote('%E4%BC%98%E5%BC%82%E6%90%9C%E7%B4%A2')
# print urllib.unquote('%E8%82%A1%E7%A5%A8')
# print urllib.unquote('%E6%96%B0%E9%97%BB%E4%B8%AD%E5%BF%83')
# print urllib.unquote('%E4%B8%8A%E5%B8%82%E5%85%AC%E5%8F%B8')
# print urllib.unquote('UOR=www.sina.com.cn,weibo.com,login.sina.com.cn; ULV=1382080934381:170:4:1:5065101321270.885.1382080934301:1381168023905; __utma=182865017.727142032.1350394937.1350394937.1350394937.1; lzstat_uv=39671918401417150031|2893156; SINAGLOBAL=2675969447680.694.1358760785269; ssoln=elevenjunjun%40sohu.com; ALF=1384972407; wvr=5; USRHAWB=usrmdins311178; SUS=SID-1946327541-1382380407-JA-hp5ck-30dd68fb2fb4ae3a42801f63625d65f8; SUE=es%3Dbcd3baba51abc8ecbe77048142b18a1d%26ev%3Dv1%26es2%3D796d18e55c35a6933c170e86f0ecaecb%26rs0%3Dx3pJvNlHZVGmau7sW5ntkqFym4uTkqz48ruR0U1bmkKZ1uFZlQv8Da4RETZQurjpa5LpeuOe6AI5MVWZBO1nppFNJHnEh9TOTNpDped0dmTmlEA5ntexOe0cbZ%252BkYO7csyj7exaMjVkxZcaSUtYzZJfMpmb3%252BcP8rrAKTidDNZo%253D%26rv%3D0; SUP=cv%3D1%26bt%3D1382380407%26et%3D1382466807%26d%3Dc909%26i%3D17c4%26us%3D1%26vf%3D0%26vt%3D0%26ac%3D2%26st%3D0%26uid%3D1946327541%26name%3Delevenjunjun%2540sohu.com%2')
# print urllib.unquote("%C3%C0%CE%B6")
# print urllib.unquote('USB%5CVID_1782%26PID_5D03%5C6%2618D0524%260%2619761202 android-device 9U82604Ibggkfbj1QMbRwNzNVtHnF49t3ARTECNX3GunHPWv7nOdgNHZ2qWme8vGBsGa3cc6tIft/LNL4iBTZA== undefined 457F39BE-4113-4BF8-A08A-9284269E5037 ')
# print urllib.unquote("5bTjNxhShoJ6bjaMBZOXiBTDpGfpESSKnmSMGxBxKDM_")
# print urllib.unquote("Vq8l%2BKCLiw%3D%3D")
# print urllib.unquote("e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0")
# print urllib.unquote("VW8dqn%2BhPU0%3D&vt3=F8dHqKwmyeHvPd1Vp2E%3D&lg2=UtASsssmOIJ0bQ%3D%3D")
print "Output: ", urllib.unquote("%0D%0A%20%0D%0A%0D%0A%20%0D%0")
raw_input()

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
#     url = "http://socialmediagroup.com/2013/10/28/teched-las-vegas-what-i-learned-what-i-saw/"
# #     url = "http://socialmediagroup.com/2008/04/28/social-media-press-releases-your-secret-weapon/"
#     html_text = get_html(url)
#     doc = fromstring(html_text)
#     urls = doc.xpath('//a/@href')
#     with open("../io/hrefs_in_one_link_v1.txt", 'w') as wf:
#         for u in urls:
#             wf.write(u + '\n')
#     pdb.set_trace()

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
    urls = ["https://www.google.com.hk/search?q=python+%E8%A7%A3%E6%9E%90url&oq=python+%E8%A7%A3%E6%9E%90url&aqs=chrome..69i57j0l2j69i64.7609j0j7&sourceid=chrome&espv=210&es_sm=93&ie=UTF-8",
           "http://product.auto.163.com/dealer/search/all_504_1684_0_%25E5%25A5%25A5%25E8%25BF%25AA_5_1.html"]
     
    for url in urls:
        parse_url(url)
        print "-" * 50
        
    #===============================================================================
    # extracting marketing attribution data (such as search terms) from referer URLs
    # 从URL中提取市场营销相关的数据（比如搜索关键字）
    #===============================================================================
#     with open("../io/url_snippet.txt") as f:
#         for line in f:
#             url = line.strip()
#             get_detailed_referer(url)
