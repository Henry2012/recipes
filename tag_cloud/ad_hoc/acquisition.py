#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: tag_cloud.ad_hoc.acquisition.py
Description: this program
Creation: 2014-1-24
Revision: 2014-1-24
"""

with open('../io/yejiyuqi_news.txt', 'w') as wf:
    with open('../io/entity_extracted_from_news.txt') as f:
        count = 0
        for i, line in enumerate(f):
            splitted = line.strip().split('\t')
            title = splitted[1]
            if '业绩预期' in title:
                #print line
                wf.write(line)
                count += 1
        print count, i + 1
