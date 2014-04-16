#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: timer.py
Description: this program just serves as a timer
Creation: 2013-11-26
Revision: 2013-11-26
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

class Timer():
    time = __import__('time')
    
    def __enter__(self):
        self.start = Timer.time.time()
        return self

    def __exit__(self, *args):
        self.end = Timer.time.time()
        self.interval = self.end - self.start