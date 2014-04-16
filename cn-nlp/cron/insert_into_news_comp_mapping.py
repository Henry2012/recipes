#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
Creation: 2014-3-4
Revision: 2014-3-4
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

import os
import pdb
import sys
basepath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(basepath, "..")))

from util import (get_stock_quote_mapping,
                  get_mysql,
                  get_db_parser,
                  transfer_datetime_to_str,
                  update_is_news_comp_mapping_done)

def insert_wholly(mysql, news_title_tname, company_tname, news_company_mapping_tname):
    insert_keys = ['news_id', 'quote', 'symbol', 'media_date']

    # 获得公司名简称与code的映射关系
    company_mapping = get_stock_quote_mapping(mysql, company_tname)

    # 获得有公司名的记录
    find_sqlstr = 'select id, quotes, media_date from %s where no_of_quotes>0' % news_title_tname
    insert_value_package = []
    for i, (id, quotes, media_date) in enumerate(mysql.find(find_sqlstr)):
        # 每1000条commit一次
        if i and not (i % 1000):
            print i
            mysql.insert_records(insert_keys, insert_value_package, news_company_mapping_tname)
            mysql.commit()
            insert_value_package = []
        quotes = quotes.strip().split('>|<')
        insert_value = [(id, quote, company_mapping[quote], transfer_datetime_to_str(media_date)) for quote in quotes]
        insert_value_package.extend(insert_value)
    else:
        mysql.insert_records(insert_keys, insert_value_package, news_company_mapping_tname)
        mysql.commit()

    #===============================================================================
    # 更新news_title_tname中的is_news_comp_mapping_done字段
    #    1. 找到值为null的字段，并且update为1
    #===============================================================================
    update_is_news_comp_mapping_done(mysql, news_title_tname)

    mysql.close()

def insert_incrementally(mysql, news_title_tname, company_tname, news_company_mapping_tname):
    insert_keys = ['news_id', 'quote', 'symbol', 'media_date']

    # 获得公司名简称与code的映射关系
    company_mapping = get_stock_quote_mapping(mysql, company_tname)

    # 获得有公司名的记录
    find_sqlstr = 'select id, quotes, media_date from %s where no_of_quotes>0 and is_news_comp_mapping_done is null' % news_title_tname
    insert_value_package = []

    #===============================================================================
    # 注意这里的mysql.execute是在mysql.insert_records中实现的。
    # 多条数据在一个sql语句中能够实现insert,而多条记录需要update时则对应多条upd_sql语句
    #===============================================================================
    for i, (id, quotes, media_date) in enumerate(mysql.find(find_sqlstr)):
        # 每1000条commit一次
        if i and not (i % 1000):
            print i
            mysql.insert_records(insert_keys, insert_value_package, news_company_mapping_tname)
            mysql.commit()
            insert_value_package = []
        quotes = quotes.strip().split('>|<')
        insert_value = [(id, quote, company_mapping[quote],
                         transfer_datetime_to_str(media_date)) for quote in quotes]
        insert_value_package.extend(insert_value)

    else:
        mysql.insert_records(insert_keys, insert_value_package, news_company_mapping_tname)
        mysql.commit()

    #===============================================================================
    # 更新news_title_tname中的is_news_comp_mapping_done字段
    #    1. 找到值为null的字段，并且update为1
    #===============================================================================
    update_is_news_comp_mapping_done(mysql, news_title_tname)

    mysql.close()

if __name__ == "__main__":
    environ = 'production'
    mysql = get_mysql(environ)
    parser = get_db_parser()
    news_title_tname = parser.get(environ, 'news_title_tname')
    company_tname = parser.get(environ, 'company_tname')
    news_company_mapping_tname = parser.get(environ, 'news_comp_mapping_tname')

    #===============================================================================
    # 全量处理
    #===============================================================================
    insert_wholly(mysql, news_title_tname, company_tname, news_company_mapping_tname)

    #===============================================================================
    # 增量处理
    #===============================================================================
    #insert_incrementally(mysql, news_title_tname, company_tname, news_company_mapping_tname)
