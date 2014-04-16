#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: stock_ups_and_downs.utils.py
Description: this program gives utilities.
Creation: 2014-1-13
Revision: 2014-1-13
"""

import datetime
import requests
import imp
import json
import os
import yaml

# URL = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=60&num=40&sort=changepercent&asc=0&node=hs_a&symbol=&_s_r_a=page"
# URL = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=2400&sort=changepercent&asc=0&node=hs_a&symbol=&_s_r_a=page"
URL = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=3000&sort=changepercent&asc=0&node=hs_a&symbol=&_s_r_a=page'
CURRENT_DIR = os.path.dirname(__file__)

def get_daily_market(url):
    r = requests.get(url)
    html_text = r.text.encode(encoding="utf-8")
    html_text = html_text.replace(':', ": ")

    # json不能解析html_text,因为每个key缺少引号，所以这里尝试使用yaml来解析。
    symbols = yaml.load(html_text)
    
    # 查看一共有多少家公司 (2437 in all)
    #print len(set(each['symbol'] for each in symbols))
    #pdb.set_trace()

    return symbols

def get_today(flag):
    # flag设置返回字符串是长字符串，还是短字符串
    if flag == "short":
        today_dtime = datetime.date.today()
        today_str = today_dtime.strftime('%Y%m%d')
    elif flag == "long":
        today_dtime = datetime.datetime.today()
        today_str = today_dtime.strftime('%Y%m%d%H%M%S')
    return today_str

def get_wfpath(flag):
    today_str = get_today(flag)
    wfname = "".join([today_str, ".json"])
    return os.path.join(CURRENT_DIR, "io", wfname)

#===============================================================================
# Drilling around: 对数据做些基础分析
#     1. symbols开头的两个字符仅是"sz" & "sh"
#     2. 将"sz002132"改成"002132.sz"
#===============================================================================

def get_all_symbols():
    symbols = set()
    with open("io/20140113.json") as f:
        for each in f:
            ticker_info = json.loads(each.split("\t")[1])
            symbol = ticker_info['symbol']
            if "sh" in symbol:
                symbol = "".join([symbol[2:], ".sh"])
            else:
                symbol = "".join([symbol[2:], ".sz"])
            symbols.add(symbol)
    return symbols

def save_all_symbols():
    symbols = list(get_all_symbols())
    with open("./io/symbols.json", 'w') as wf:
        wf.write(json.dumps(symbols))
        
if __name__ == "__main__":
#     print get_all_symbols()
    save_all_symbols()