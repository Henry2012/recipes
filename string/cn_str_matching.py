#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: sundries.cn_str_matching.py
Description: this program
Creation: 2014-2-17
Revision: 2014-2-17
"""

print "我是中国人：".endswith('：')

#===============================================================================
# 替换所有空格（包含全角空格及一般的空格）
#     1. replace(' ', '，') 一般的空格
#     2. replace('　', '，') 全角空格
#===============================================================================

title = '五粮液，推出中价位产品　调整期寻新发展。'
new_title = title.replace(' ', '，').replace('　', '，')
print new_title
print title.replace(' ', '，')