#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: is_number.py
Description: this program checks whether a string is a number.
Creation: 2013-11-7
Revision: 2013-11-7
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

#===============================================================================
# Check whether a string is a number
#===============================================================================
def is_number(s):
    try:
        float(s)
    except ValueError:
        return False
    else:
        return True

if __name__ == "__main__":
    
    assert is_number('-0.3') == True
    assert is_number('1234000000000000000000000000') == True
    assert is_number('000000000012340000000') == True