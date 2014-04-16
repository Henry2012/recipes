#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: general_testbox.test_property_decorator.test_property_v2.py
Description: 
Creation: 2013-10-16
Revision: 2013-10-16
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

class C(object):
    def __init__(self):
        self._x = 10
        
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, a):
        self._x = a
        return self._x
    
if __name__ == "__main__":
    c = C()
    print c.x
    
    c.x = 20
    
    print c.x