# -*- coding: utf-8 -*-

'''
Created on 2013-9-26

@author: Qiqun.H

http://stackoverflow.com/questions/42558/python-and-the-singleton-pattern
'''

class Singleton(object):
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
            
        return cls._instance


if __name__ == "__main__":
    s1 = Singleton()
    s2 = Singleton()
    
    if s1 is s2:
        print "Same"
    else:
        print "Different"
