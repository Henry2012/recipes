#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: decorator.recipe.py
Description: this program
Creation: 2014-4-16
Revision: 2014-4-16
"""

def makeitalic(fn):
    def wrapper():
        return "<i>" + fn() + '</i>'
    
    return wrapper

def makebold(fn):
    def wrapper():
        return "<b>" + fn() + '</b>'
    
    return wrapper

@makeitalic
@makebold
def hello():
    return "Hello World!"

if __name__ == "__main__":
    print hello()
