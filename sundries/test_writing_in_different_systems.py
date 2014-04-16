#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: sundries.test_writing_in_different_systems.py
Description: this program
Creation: 2014-1-16
Revision: 2014-1-16
"""

with open("../io/test.txt", 'w') as wf:
    wf.write("1\r\n")
    wf.write("2\n")
    wf.write("3\r\n")