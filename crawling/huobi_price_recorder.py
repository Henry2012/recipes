#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: crawling.crawl_btc123.py
Description: this program crawls data from huobi.com
Creation: 2014-1-7
Revision: 2014-1-7
"""

import os
import re
import requests
import sys
import datetime

basepath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(basepath, "..")))

reload(sys)
sys.setdefaultencoding('utf-8')

# btc123 火币网报价接口
btc123_huobi = "http://www.btc123.com/e/interfaces/tickers.js?type=huobiTicker&s=59114"

# 使用requests连接该接口
r = requests.get(btc123_huobi)

# 获取当前的时间
right_now = datetime.datetime.now()
right_now = right_now.strftime('%Y%m%d%H%M%S')

# 获得接口提供的数据
result = r.json()
last_price = result['ticker']['last']

# 将当前成交价格以append方式写入文件
with open("/mnt/share/gitStuff/recipes/io/huobi_price_recorder.txt", "a") as wf:
    text = "\t".join([right_now, last_price])
    wf.write(text + "\n")
