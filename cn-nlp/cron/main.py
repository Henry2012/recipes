#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
Creation: 2014-3-12
Revision: 2014-3-12
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

import os
import sys
basepath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(basepath, "..")))

from util import (get_mysql,
                  get_db_parser)
from news_crawler_processing.insert import insert_incrementally as insert_raw_news_incrementally
from preprocessing import preprocess_in_mysql_incrementally
from insert_into_news_comp_mapping import insert_incrementally as insert_news_comp_mapping_incrementally

def daily_processing(environ, fname):
    parser = get_db_parser()
    mysql = get_mysql(environ)
    news_title_tname = parser.get(environ, 'news_title_tname')
    company_tname = parser.get(environ, 'company_tname')
    news_company_mapping_tname = parser.get(environ, 'news_comp_mapping_tname')
    crawled_news_dir = parser.get(environ, 'crawled_news_dir')

    insert_raw_news_incrementally(mysql, fname, crawled_news_dir, news_title_tname)

    mysql = get_mysql(environ)
    preprocess_in_mysql_incrementally(mysql, news_title_tname, company_tname)

    mysql = get_mysql(environ)
    insert_news_comp_mapping_incrementally(mysql, news_title_tname, company_tname, news_company_mapping_tname)

if __name__ == "__main__":
    concerned_date = sys.argv[1]
    fname = concerned_date + '.txt'
    daily_processing('production', fname)
