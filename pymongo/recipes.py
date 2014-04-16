#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: pymongo.recipes.py
Description: this program deals with pymongo operation.
Creation: 2013-11-6
Revision: 2013-11-6
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

import pymongo
from config import uri

#===============================================================================
# Authenticate
#===============================================================================
client = pymongo.MongoClient(uri)

db = client.ES_raw_data
collection = db['angellist']  # collection = db.angellist
for each in collection.find_one():
    pass

#===============================================================================
# some query examples
# $ne
# $elemMatch
# $nin
# more grammars could be referenced from Evernote.
#===============================================================================
collection.find({"company_type": {"$ne": []}})
collection.find({"markets": {"$ne": []}})
collection.find({"company_type": {"$elemMatch": {"display_name": "Acquired"}}})
collection.find({"$and": [{"company_type": {"$elemMatch": {"display_name": "Acquired"}}},
                          {"markets": {"$elemMatch": {"display_name": "Marketplaces"}}}]})

#===============================================================================
# Alternative way of authenticate
#===============================================================================
# client = pymongo.MongoClient('example.com')
# client.the_database.authenticate('user', 'password')

#===============================================================================
# Search based on string value
# Search records with "big data" in tag_list
#===============================================================================

#===============================================================================
# 显示出一个字段下所有distinct values
#    在mongo javascript shell下，使用db.mycoll.distinct('tags', {'category': "movie"})
#    如何在pymongo下实现这样的功能
#===============================================================================

db.mycoll.find({'category': "movie"}).distinct("tags")

#===============================================================================
# close mongo connection
#===============================================================================

client.close()
# client.disconnect()
