#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: general_testbox.test_property_decorator.test_property.py
Description: 
Creation: 2013-10-16
Revision: 2013-10-16
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

class C(object):
    def __init__(self):
        self._x = None

    @property
    def x(self):
        """I'm the 'x' property."""
        return self._x

    @x.setter
    def x(self, value):
        if value > 10:
            raise ValueError('this value is too large.')
        else:
            self._x = value

    @x.deleter
    def x(self):
        del self._x
        
if __name__ == "__main__":
    c = C()
    c.x = 6
    print c.x
    print c._x
