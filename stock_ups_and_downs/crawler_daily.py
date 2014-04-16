#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: stock_ups_and_downs.crawler.py
Creation: 2014-1-10
Revision: 2014-1-10
"""

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import json
from utils import (get_daily_market,
                   get_wfpath,
                   URL)

def save_daily_market():
    # 这里的参数只有"long" & "short"
    wfpath = get_wfpath("long")

    daily_market_info = get_daily_market(URL)

    with open(wfpath, "w") as wf:
        for ticker in daily_market_info:
            ticker_name = ticker['name']
            line = '\t'.join([ticker_name, json.dumps(ticker) + "\n"])
            #print type(line)
            #line = line.encode('utf8')
            wf.write(line)

if __name__ == "__main__":
    save_daily_market()
