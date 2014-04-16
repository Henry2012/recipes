#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: sundries.quiz.py
Description: this program
Creation: 2014-4-2
Revision: 2014-4-2
"""

adders = []
for i in range(0, 100):
    adders.append(lambda x: x + i)
print adders[0](0)
print adders[1](0)
print adders[2](0)
# for i, each in enumerate(adders):
#     if i > 20:
#         break
#     print i, each(0)

# print adders[17](0)
# print adders[17](42)