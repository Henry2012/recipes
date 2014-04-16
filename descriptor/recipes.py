#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: descriptor.recipes.py
Description: this program
Creation: 2014-3-6
Revision: 2014-3-6
"""

class RevealAccess(object):
    """A data descriptor that sets and returns values
       normally and prints a message logging their access.
    """

    def __init__(self, initval=None, name='var'):
        self.val = initval
        self.name = name

    def __get__(self, obj, objtype):
        print 'Retrieving', self.name
        return self.val

    def __set__(self, obj, val):
        print 'Updating', self.name
        self.val = val

class MyClass(object):
    x = RevealAccess(10, 'var "x"')
    y = 5
    
class Movie(object):
    def __init__(self, title, rating, runtime, budget, gross):
        self.title = title
        self.rating = rating
        self.runtime = runtime
        self.gross = gross
        if budget < 0:
            raise ValueError("Negative value not allowed: %s" % budget)
        self.budget = budget
        
    def profit(self):
        return self.gross - self.budget

if __name__ == "__main__":
    
#     m = MyClass()
#     print m.x
#     print m.y
#     print dir(m)
#     print m.__dict__
#     print RevealAccess().__dict__

    m = Movie('Frozen', '4', '2014-1-1', 3000, 4000)
    print m.profit()
    m.gross = 1000
    print m.profit()
    m.budget = -1000
    print m.profit()