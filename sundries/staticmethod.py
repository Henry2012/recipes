#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: sundries.staticmethod.py
Description: this program
Creation: 2014-2-10
Revision: 2014-2-10
"""

class MyClass(object):
    @staticmethod
    def display(name):
        print "Hello %s.\n" % name

if __name__ == "__main__":
    MyClass.display('qiqun')
    
    m = MyClass()
    m.display('qq')