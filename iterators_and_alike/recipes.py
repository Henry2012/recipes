#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: iterators_and_alike.recipes.py
Description: this program
Creation: 2014-3-7
Revision: 2014-3-7
"""

import time

#===============================================================================
# A method to build an iterator
#===============================================================================

class CountDown(object):
    def __init__(self):
        self._remaining = [1, 2, 3, 4, 5, 'launch']
    
    def __iter__(self):
        return self
    
    def next(self):
        if not self._remaining:
            raise StopIteration
        return self._remaining.pop(0)

#===============================================================================
# A second method to build an iterator
#===============================================================================

class SecondCountDown(object):
    def __iter__(self):
        for each in [1, 2, 3, 4, 5, 'launch']:
            yield each
            
#===============================================================================
# A method to build a generator
#===============================================================================

def countdown_generator():
    for each in [1, 2, 3, 4, 5, 'launch']:
        yield each

#===============================================================================
# slow generator
#===============================================================================

def slow_generator():
    time.sleep(5)
    yield 5
    time.sleep(1)
    yield 4
    time.sleep(1)
    yield 3
    time.sleep(1)
    yield 2
    time.sleep(1)
    yield 1
    time.sleep(1)

def slow_gen():
    for each in zip(range(5, 0, -1), [5, 1, 1, 1, 1]):
        yield each

def knock_knock():
    name = yield "Who's there?"
    yield "%s who?" % name
    yield "That's not funny at all"

if __name__ == "__main__":
    
#     c = CountDown()
#     c2 = SecondCountDown()
#     c3 = countdown_generator()
#     c4 = slow_generator()
    
#     print c.next()
#     print c.next()
#     print c.next()
#     print c.next()
    
#     for each in c:
#         print each
# 
#     for each in c2:
#         print each
#         
#     for each in c3:
#         print each
#         
#     print 'Starting...'
#     for each in c4:
#         print each
#     print 'End...'
    
#     print 'Starting...'
#     for counter, time_period in slow_gen():
#         time.sleep(time_period)
#         print counter
#     print 'End...'

    d = knock_knock()
    print d.next()
    print d.send('Qiqun')
    print d.next()
