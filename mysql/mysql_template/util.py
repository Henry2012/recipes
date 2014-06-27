#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
Creation: 2014-4-30
Revision: 2014-4-30
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

import os
from ConfigParser import SafeConfigParser
from mysqlAPI import Mysql

CURRENT_DIR = os.path.dirname(__file__)

#===============================================================================
# 获取db相关的配置
#===============================================================================

def get_mysql(environ):
    parser = get_db_parser()
    host = parser.get(environ, 'host')
    port = parser.getint(environ, 'port')
    user = parser.get(environ, 'user')
    pwd = parser.get(environ, 'pwd')
    dbname = parser.get(environ, 'dbname')

    mysql = Mysql(host, port, user, pwd, dbname)
    return mysql

def get_db_parser():
    db_cfg_fpath = os.path.join(CURRENT_DIR, 'db.cfg')
    parser = SafeConfigParser()
    parser.read(db_cfg_fpath)

    return parser