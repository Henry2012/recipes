#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: arsenal.nlp.similarity.levenshtein_by_Levenshtein.py
Description: this program calculates levenshtein distances
Creation: 2013-10-17
Revision: 2013-10-17
"""

#===============================================================================
# easy_install python-Levenshtein
# https://pypi.python.org/pypi/python-Levenshtein/

# "A C extension module for fast computation of:
# - Levenshtein (edit) distance and edit sequence manipulation
# - string similarity
# - approximate median strings, and generally string averaging
# - string sequence and set similarity

# Levenshtein has some overlap with difflib (SequenceMatcher).
# It supports only strings, not arbitrary sequence types, but on the other hand it's much faster.
# It supports both normal and Unicode strings, but can't mix them, all arguments to a function (method)
# have to be of the same type (or its subclasses).

# 常用的方法有：
# distance： 编辑距离，是描述由一个字符串转化成另一个字符串最少的操作次数。允许的操作有：插入、删除、替换
# ratio： 计算公式r=(sum-dist)/sum.其中sum是两字符串的长度之和，dist是类编辑距离，插入和删除的权重为1，替换的权重为2。而对于编辑距离，三种操作方式的权重都为1.
# hamming: 汉明距离，要求两个字符串必须长度一致，是描述两个等长字符串之间对应位置上不同字符的个数

# 完整的方法列表详见：
# http://www.coli.uni-saarland.de/courses/LT1/2011/slides/Python-Levenshtein.html#Levenshtein-inverse
#===============================================================================

import Levenshtein

if __name__ == "__main__":
    text1 = "创业板暴跌4.37% 现巨阴断头铡"
    text2 = "创业板暴跌4.37% 现巨阴断头铡"
    
    print Levenshtein.ratio(text1, text2)
    
    #print Levenshtein.hamming('aa12', 'adfc')
    
    #print Levenshtein.distance('abcd', 'adc')
