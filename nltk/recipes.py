#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: nltk.recipes.py
Description: this program
Creation: 2014-2-10
Revision: 2014-2-10
"""

#===============================================================================
# 如何区别ConditionalFreqDist & FreqDist的使用场景
#===============================================================================

from nltk import FreqDist as FD
from nltk import ConditionalFreqDist as CFD

data = (('woman', ('this', 'bought')),
        ('man', ('this', 'looked')))

c = CFD(data)

# 返回FreqDist object
print c['woman']

# 下面两个statements是等价的
print c['woman'][('this', 'bought')]
print c['woman'].freq(('this', 'bought'))

# 尝试访问不存在的condition
print c['a']

# 利用相同的数据测试在FD下的结果
f = FD(data)
print f

# 尝试没有提供数据时的初始化结果
print CFD()

#===============================================================================
# 测试plot
#===============================================================================

import matplotlib
import matplotlib.pyplot as plt

f.plot(cumulative=True)