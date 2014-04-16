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
btc123_huobi = "http://www.btc123.com/e/interfaces/tickers.js?type=huobiTicker"
btc123_btcchina = "http://www.btc123.com/e/interfaces/tickers.js?type=btcchinaTicker"
btc123_okcoin = "http://www.btc123.com/e/interfaces/tickers.js?type=okcoinTicker"
btc123_chbtc = "http://www.btc123.com/e/interfaces/tickers.js?type=chbtcTicker"
btc123_btc100 = "http://www.btc123.com/e/interfaces/tickers.js?type=btc100Ticker"

urls = {'huobi': btc123_huobi,
	'btcchina': btc123_btcchina, 
	'okcoin': btc123_okcoin,
        'chbtc': btc123_chbtc,
	'btc100': btc123_btc100}

# 获取当前的时间
def get_recent_time():
    right_now = datetime.datetime.now()
    right_now = right_now.strftime('%Y%m%d%H%M%S')
    return right_now

# 使用requests连接接口，获得各个平台的BTC价格
def get_difference():
    prices = []
    for ticker, url in urls.iteritems():
        r = requests.get(url)
        # 获得接口提供的数据
        result = r.json()
        last_price = float(result['ticker']['last'])
        prices.append([ticker, last_price])
    
    sorted_prices = sorted(prices, key=lambda k: k[1])
    max_ticker, max_price = sorted_prices[-1]
    min_ticker, min_price = sorted_prices[0]
    
    difference = max_price - min_price
    percent = difference / min_price

    return percent, difference, max_ticker, min_ticker, min_price

if __name__ == "__main__":
    right_now = get_recent_time()
    difference = get_difference()
    #print map(str, difference)

    # map() gives a list, while string format requires tuple.
    # so tuple() is required
    #print type(map(str, difference))

    output = "Percent:%.3f\tDifference:%.3f\tMax:%s\tMin:%s\tMinPrice:%.3f\n" % difference
    #print output

    # 存储当前中国市场btc价差
    with open("/mnt/share/gitStuff/recipes/io/chinese_btc_difference.txt", "a") as wf:
        text = "\t".join([right_now, output])
        wf.write(text)
