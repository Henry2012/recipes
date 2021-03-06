#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: str.recipes.py
Description: this program
Creation: 2014-2-19
Revision: 2014-2-19
"""

#===============================================================================
# 可以通过设置数量值的str方法
#===============================================================================

# 替换所有的a为z
print 'abca'.replace('a', 'z')
# 只替换第一个出现的a为z
print 'abca'.replace('a', 'z', 1)

print 'abc de fg'.split(' ')
# 只切分第一个出现的空格
print 'abc de fg'.split(' ', 1)

#===============================================================================
# 一些匹配方法
#===============================================================================

print 'asdf'.isalnum()
print 'asdf'.isalpha()
