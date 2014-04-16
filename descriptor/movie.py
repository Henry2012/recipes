#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: descriptor.movie.py
Description: this program
Creation: 2014-3-6
Revision: 2014-3-6
"""

class Movie(object):
    def __init__(self, title, rating, runtime, budget, gross):
        self._budget = None

        self.title = title
        self.rating = rating
        self.runtime = runtime
        self.gross = gross
        self.budget = budget
        
    @property
    def budget(self):
        return self._budget
    
    @budget.setter
    def budget(self, value):
        if value < 0:
            raise ValueError("Negative value not allowed: %s" % value)
        self._budget = value
        
    def profit(self):
        return self.gross - self.budget

    
m = Movie('Casablanca', 97, 102, 964000, 1300000)
print m.budget       # calls m.budget(), returns result
try:
    m.budget = -100  # calls budget.setter(-100), and raises ValueError
except ValueError:
    print "Woops. Not allowed"