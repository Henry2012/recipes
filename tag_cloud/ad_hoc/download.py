#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: tag_cloud.ad_hoc.download.py
Description: this program
Creation: 2014-1-24
Revision: 2014-1-24
"""

import os
import sys
basepath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(basepath, "..")))

from mysqlAPI import Mysql

host = "esdev-mysql.cloudapp.net"
port = 3306
user = "esapp"
pwd = "esapp1"
dbname = "mscndemo"
db = Mysql(host, port, user, pwd, dbname)

