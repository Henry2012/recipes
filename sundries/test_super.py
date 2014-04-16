#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: sundries.test_super.py
Description: this program
Creation: 2014-3-18
Revision: 2014-3-18
"""

import logging

class Base(object):
    def __init__(self):
        print "Base created"

class ChildA(Base):
    def __init__(self):
        Base.__init__(self)

class ChildB(Base):
    def __init__(self):
        super(ChildB, self).__init__()

print ChildA()
print '-' * 50
print ChildB()

#===============================================================================
# LoggingDict
#===============================================================================

class LoggingDict(dict):
    def __setitem__(self, key, value):
        logging.info('Setting %r to %r' % (key, value))
        super(LoggingDict, self).__setitem__(key, value)

logD = LoggingDict()
logD['a'] = 1
print logD