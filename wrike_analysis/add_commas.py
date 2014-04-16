#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: news_stat.add_commas.py
Description: this program
Creation: 2013-12-5
Revision: 2013-12-5
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

#===============================================================================
# 只提取出Counter部分，并为此生成一个可以放在ipnb中处理的格式（如下）
#     1,
#     2,
#     1,
#===============================================================================

with open("../io/wrike_news_stat_v2.txt", "w") as wf:
    with open("../io/wrike_news_stat.txt") as f:
        for line in f:
            line = line.strip().split('\t')[1] + "," + "\n"
            wf.write(line)
