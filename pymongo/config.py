#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: pymongo.config.py
Description: this program provides config of mongod
Creation: 2013-11-5
Revision: 2013-11-5
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

host = 'ec2-23-21-130-73.compute-1.amazonaws.com'
database = 'admin'
username = 'dbadmin'
password = 'botoinfoAdmin2013'

uri = "mongodb://%s:%s@%s/%s" % (username, password,
                                 host, database)

