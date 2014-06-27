#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: copy_reg.recipe.py
Description: this program
Creation: 2014-4-17
Revision: 2014-4-17
"""

import copy_reg
import copy
import pickle

class Foo(object):
    def __init__(self, a):
        self.a = a
    
def pickle_c(c):
    print("pickling a C instance...")
    return Foo, (c.a,)

copy_reg.pickle(Foo, pickle_c)
c = Foo(1)
d = copy.copy(c)
p = pickle.dumps(c)