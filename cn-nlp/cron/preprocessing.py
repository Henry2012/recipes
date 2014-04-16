#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
Creation: 2014-2-24
Revision: 2014-2-24
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

import os
import pdb
import sys
basepath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(basepath, "..")))

from mysqlAPI import Mysql
from timer import Timer
from util import (get_related_companies,
                  contains_blank,
                  contains_colon,
                  contains_zhengquan,
                  contains_hyphen,
                  contains_quote_before_colon,
                  get_db_parser,
                  get_update_sqlstr,
                  get_mysql,
                  get_stock_quote_mapping)

def preprocess(title, stock_quotes):
    '''
    [quotes, no_of_quotes, contains_colon,
    contains_blank, contains_zhengquan,
    contains_hyphen, contains_quote_before_colon]
    '''
    title = title.replace(":", "：").replace('　', ' ')

    quotes = get_related_companies(title, stock_quotes)
    quotes_in_str = ">|<".join(quotes)
    no_of_quotes = len(quotes)
    contains_blank_flag = int(contains_blank(title))
    contains_colon_flag = int(contains_colon(title))
    contains_hyphen_flag = int(contains_hyphen(title))
    contains_zhengquan_flag = int(contains_zhengquan(quotes))
    contains_quote_before_colon_flag = int(contains_quote_before_colon(title, quotes))

    # revised_title
    revised_title = title + '。'
    if contains_colon_flag:
        if no_of_quotes == 1:
            if not contains_zhengquan_flag:
                if contains_quote_before_colon_flag:
                    # 唯一的公司名在第一个冒号之前
                    # 1. 将冒号改成中文逗号
                    # 2. 将空格也改成中文逗号
                    revised_title = revised_title.replace('：', '，').replace(' ', '，')
                else:
                    # 唯一的公司名在第一个冒号之后
                    # 1. 去除第一个冒号及之前的所有的内容
                    # 2. 将空格也改成中文逗号
                    if not title.endswith("："):
                        revised_title = revised_title.split("：", 1)[1].replace(' ', '，')
        elif no_of_quotes > 1:
            if (not contains_zhengquan_flag and
                not contains_hyphen_flag):
                if contains_quote_before_colon_flag:
                    # 至少一个公司名在第一个冒号之前
                    # 1. 将冒号改成中文逗号
                    # 2. 将空格也改成中文逗号
                    revised_title = revised_title.replace('：', '，').replace(' ', '，')
                else:
                    # 所有的公司名都在第一个冒号之后
                    # 1. 去除第一个冒号及之前的所有的内容
                    # 2. 将空格也改成中文逗号
                    if not title.endswith("："):
                        revised_title = revised_title.split("：", 1)[1].replace(' ', '，')
    elif contains_blank_flag:
        revised_title = revised_title.replace(' ', '，')

    revised_title = revised_title.replace('《', ' ').replace("》", " ")
    revised_title = revised_title.replace("‘", ' ').replace('’', ' ')
    revised_title = revised_title.replace('“', ' ').replace('”', ' ')
    revised_title = revised_title.replace('"', ' ').replace("'", ' ')
    return [quotes_in_str,
            no_of_quotes,
            contains_blank_flag,
            contains_colon_flag,
            contains_hyphen_flag,
            contains_zhengquan_flag,
            contains_quote_before_colon_flag,
            revised_title]

def preprocess_in_mysql_incrementally(mysql, news_title_tname, company_tname):
    # 获得所有股票名简称
    STOCK_QUOTES = set(get_stock_quote_mapping(mysql, company_tname).keys())

    #===============================================================================
    # 获得所有records，并对其进行分析
    #===============================================================================

    news_title_upd_keys = ['quotes', 'no_of_quotes',
                           'contains_blank', 'contains_colon',
                           'contains_hyphen', 'contains_zhengquan',
                           'contains_quote_before_colon', 'revised_title']
    find_all_sqlstr = "select id, title from %s where no_of_quotes is null" % news_title_tname
    with Timer() as t:
        for i, (record_id, title) in enumerate(mysql.find(find_all_sqlstr)):
            if not (i % 1000):
                mysql.commit()
                print i

            upd_values = preprocess(title, STOCK_QUOTES)

            news_title_upd_sqlstr = get_update_sqlstr(news_title_tname, news_title_upd_keys, upd_values, record_id)
            mysql.execute(news_title_upd_sqlstr)
        mysql.commit()
    mysql.close()
    print t.interval

if __name__ == "__main__":
    environ = 'local'
    parser = get_db_parser()
    mysql = get_mysql(environ)
# 
#     news_title_tname = parser.get(environ, 'news_title_tname')
    company_tname = parser.get(environ, 'company_tname')
#     
#     preprocess_in_mysql_incrementally(mysql, news_title_tname, company_tname)
    
    STOCK_QUOTES = set(get_stock_quote_mapping(mysql, company_tname).keys())
    title = u'[广发证券] 广发证券晨会纪要100406'
    preprocess(title, STOCK_QUOTES)[-3]
    
    mysql.close()
    