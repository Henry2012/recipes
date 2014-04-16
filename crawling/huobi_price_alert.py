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
basepath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(basepath, "..")))

from send_gmail import send_btc
reload(sys)
sys.setdefaultencoding('utf-8')

# btc123 火币网报价
btc123_huobi = "http://www.btc123.com/e/interfaces/tickers.js?type=huobiTicker&s=59114"

# 新浪财经提供的大部分btc交易平台的报价
sina_url = "http://hq.sinajs.cn/list=btc_MtGox,btc_bitstamp,btc_btcchina,btc_btctrade,btc_chbtc,btc_fxbtc,btc_huobi,btc_okcoin"

r = requests.get(btc123_huobi)
html_text = r.text.encode(encoding="utf-8")

result = r.json()
last_price = int(result['ticker']['last'])
#print last_price

def alert():
    if last_price < 4500:
        text = "火币网---价格低于4500"
        send_btc(text)
    elif last_price > 5500:
        text = "火币网---价格高于5500"
        send_btc(text)

if __name__ == "__main__":
    
    alert()
