#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: dpark.recipes.py
Description: this program
Creation: 2013-12-12
Revision: 2013-12-12
"""

import dpark
file = dpark.textFile("../io/socialmediagroup_hrefs.txt")
words = file.flatMap(lambda x:x.split()).map(lambda x:(x,1))
wc = words.reduceByKey(lambda x,y:x+y).collectAsMap()
print wc