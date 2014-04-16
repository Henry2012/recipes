#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: general_testbox.test_multiprocessing.test_multiprocessing.py
Description: this program
Creation: 2013-11-20
Revision: 2013-11-20
"""

from multiprocessing import Pool

def multi_writing():
    pool = Pool()
    threads = [pool.apply_async(_func, [chunk]) for chunk in _chunks()]
    
    for t in threads:
        t.get()

def _func(batch_iterable):
    with open('../../io/test.txt', 'a') as wf:
        for each in batch_iterable:
            wf.write(each + '\n')

def _chunks():
    for i in xrange(1, 1000):
        yield "a" * i

if __name__ == "__main__":
    multi_writing()