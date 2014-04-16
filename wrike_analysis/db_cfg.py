#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
Creation: 2014-1-2
Revision: 2014-1-2
"""

#===============================================================================
# Wrike Database
#===============================================================================

host2 = "ec2-54-211-66-190.compute-1.amazonaws.com"
database2 = 'wrike'
username2 = 'guest'
password2 = 'wrike_guest'

wrike_uri = "mongodb://%s:%s@%s/%s" % (username2, password2,
                                       host2, database2)
