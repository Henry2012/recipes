#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: .py
Description: this program
Creation: 2014-1-27
Revision: 2014-1-27
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

import os
import sys
basepath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(basepath, "..")))

from ConfigParser import SafeConfigParser
from mysqlAPI import Mysql
from event_extractor import (process_acquisition,
                             process_earnings,
                             process_zhenchi,
                             process_gaining_stock,
                             process_product_release)
from util import (get_update_sqlstr,
                  UPDATE_KEYS)

def update_records_based_on_one_func(func, mysql, find_sqlstr,
                                     stock_quotes, upd_tname, upd_keys):
    for record in mysql.find(find_sqlstr):
        #print record
        #print type(record)

        record_id = int(record[0])
        title = record[1]
        output = func(title, stock_quotes)

        if output:
            # display
            #print id, output
            #print output[1][0]

            # sql
            upd_sqlstr = get_update_sqlstr(output, upd_tname, upd_keys, record_id)
            #print upd_sqlstr

            # execute sql
            mysql.execute(upd_sqlstr)

    mysql.commit()

def update_records_based_on_all(funcs):
    parser = SafeConfigParser()
    cfg_fpath = os.path.join(basepath, 'db.cfg')
    parser.read(cfg_fpath)

    host = parser.get('production', 'host')
    port = parser.getint('production', 'port')
    user = parser.get('production', 'user')
    pwd = parser.get('production', 'pwd')
    dbname = parser.get('production', 'dbname')
    event_alpha_tname = 'event_alpha'
    company_tname = 'company'

    mysql = Mysql(host, port, user, pwd, dbname)

    stock_quote_sqlstr = 'select * from %s' % company_tname
    #find_1k_sqlstr = "select id, title from %s where id < 1000 and processed is null" % event_alpha_tname
    find_sqlstr = "select id, title from %s where processed is null" % event_alpha_tname

    # 获得所有股票名简称
    STOCK_QUOTES = [each[2] for each in mysql.find(stock_quote_sqlstr)]

    for func in funcs:
        update_records_based_on_one_func(func, mysql, find_sqlstr,
                                         STOCK_QUOTES, event_alpha_tname, UPDATE_KEYS)

    mysql.close()

if __name__ == "__main__":
    funcs = (process_acquisition,
             process_earnings,
             process_zhenchi,
             process_gaining_stock,
             process_product_release)
    update_records_based_on_all(funcs)

