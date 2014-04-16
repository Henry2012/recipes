#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: crawling.pattern_matching.py
Description: this program
Creation: 2013-11-26
Revision: 2013-11-26
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

from lxml import html as h
from lxml.html import fromstring
import json
import os
import pickle
import pdb
import re
import sys
basepath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(basepath, "..")))

from pprint import pprint
from href_in_soup import (href_of_html_v5, href_of_html_v2,
                          href_of_html_v3)

from timer import Timer

# with open('../io/signal_pattern.pkl', 'rb') as f:
#     d = pickle.load(f)
#     patterns = d.keys()

# with open("../io/patterns.txt", 'w') as wf:
#     for pattern in patterns:
#         wf.write(pattern + '\n')
# pattern = patterns[0]
#pdb.set_trace()

with open("../io/patterns.txt") as f:
    patterns = [line.strip() for line in f]

def contains_pattern_in_html_v0(patterns, html):
    flag = []
    for pattern in patterns:
        if pattern in html:
            flag.append(1)
        else:
            flag.append(0)
            
    return flag

def contains_pattern_in_html_v00(patterns, html):
    flag = []
#     extracted = []
    
    if isinstance(html, unicode):
        html = html.encode('utf8')

    doc = fromstring(html)
    extracted = doc.xpath('//a/@href')

    for each in doc.xpath('//script'):
        t = each.text
        if t:
            extracted.append(t)
    
    for pattern in patterns:
        for each in extracted:
            if pattern in each:
#                 print "<" * 50
#                 print h
#                 print "--->", pattern
#                 print "<" * 50
                flag.append(1)
                break
        else:
            flag.append(0)
            
    return flag

def contains_pattern_in_html_v1(patterns, html):
    flag = []
    hrefs = href_of_html_v2(html)
    
    for pattern in patterns:
        for h in hrefs:
            if pattern in h:
                flag.append(1)
        else:
            flag.append(0)
            
    return flag

def contains_pattern_in_html_v2(patterns, html):
    flag = []
    hrefs = href_of_html_v3(html)
    
    for pattern in patterns:
        for h in hrefs:
            if pattern in h:
                flag.append(1)
        else:
            flag.append(0)
            
    return flag

def contains_pattern_in_html_v3(patterns, html):
    flag = []
    hrefs = href_of_html_v5(html)
    
    for pattern in patterns:
        for h in hrefs:
            if pattern in h:
                flag.append(1)
        else:
            flag.append(0)
            
    return flag

# def contains_pattern_in_html_v4(patterns, html):
#     doc = h.fromstring(html)
# 
#     for pattern in patterns:
#         
#     return pattern in doc

# def contains_pattern_in_html_v5(pattern, html):
#     p = re.compile(pattern)
#     return re.search(p, html)


def performance_test():
    #===============================================================================
    # v0: 最简单的,使用in
    # v1: 使用beautifulsoup提取出所有href再匹配
    # v2: 使用正则表达式提取出所有href再匹配
    # v3: 使用lxml提取出所有href再匹配
    # v4: 利用lxml索引html，再通过in来匹配
    #===============================================================================
    funcs = ['contains_pattern_in_html_v0',
             'contains_pattern_in_html_v00']

#              'contains_pattern_in_html_v1',
#              'contains_pattern_in_html_v2',
#              'contains_pattern_in_html_v3']

#              'contains_pattern_in_html_v4',
#              'contains_pattern_in_html_v5']
    
    pair_time = []
    recall_compare = []
    patterns_in_script = set([])
    with open('../io/test_100.json') as of:
        for lineno, line in enumerate(of):
            record = json.loads(line.strip())
            html = record['html']
            print "lineno is %s" % (lineno + 1)
            if html is None:
                continue
            
            pattern_compare = []
            time_compare = []
            for id, func in enumerate(funcs):
                with Timer() as t:
                    flag = eval(func)(patterns, html)
                timer_consumed = t.interval

                print "Timer consumed for the %sth algorithm: %s" % (id + 1, timer_consumed)
                matching_patterns = [patterns[i] for i, f in enumerate(flag) if f]
                
                if id == 1:
                    patterns_in_script.update(matching_patterns)

                pprint(matching_patterns)
                pattern_compare.append(matching_patterns)
                time_compare.append(timer_consumed)
                print "-" * 25
                
            more = set(pattern_compare[0])
            less = set(pattern_compare[1])
            assert less.issubset(more)
            
            if len(more) == 0:
                recall = 100
            else:
                recall = float(len(less)) / len(more) * 100
            recall_compare.append(recall)
            print "Recall for the 2nd algorithm: ", recall
            
            pair_time.append(time_compare)
            print "-" * 50
            
    print "Average of recall: ", sum(recall_compare) / float(len(recall_compare))
    print "Average of time consumed for 1st algorithm: ", sum(each[0] for each in pair_time) / float(len(pair_time))
    print "Average of time consumed for 2nd algorithm: ", sum(each[1] for each in pair_time) / float(len(pair_time))
    print len(patterns_in_script)
    
    with open("../io/patterns_occurred_in_script.txt", 'w') as wf:
        for each in patterns_in_script:
            wf.write(each + '\n')
#     pdb.set_trace()

if __name__ == "__main__":
    performance_test()
