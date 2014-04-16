#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: chinese_word_seg.recipes.py
Description: this program
Creation: 2013-11-13
Revision: 2013-11-13
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

import codecs
import pdb
import jieba

text = u"理货员岗位职责"
text = u"上海青浦有发展潜力吗"

#===============================================================================
# 加载自定义字典进行中文分词
#===============================================================================

jieba.load_userdict('mydict.txt')
s = ">|<".join(jieba.cut(text))

#===============================================================================
# 利用a模式可以写入文本，可利用w模式无法写入文本
#===============================================================================

with open("../io/_test.txt", 'w') as wf:
    wf.write(s)

# with codecs.open('../io/_test.txt', 'w', 'utf-8') as wf:
#     wf.write(s)

# wf = codecs.open('../io/_test.txt', 'w', 'utf-8')
# wf.write(s)
# wf.close()

#===============================================================================
# 判断汉字字符串长度时需要转换成Unicode,不然结果不正确
#===============================================================================
# text = unicode("韩启群", encoding='utf8', errors='ignore')
# 
# print len(text)