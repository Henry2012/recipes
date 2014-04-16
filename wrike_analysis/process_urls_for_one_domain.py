#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: news_stat.process_urls_for_one_domain.py
Description: this program extracts some domain stat.
Creation: 2014-1-4
Revision: 2014-1-4
"""

import json
import tldextract
from collections import defaultdict

#===============================================================================
# 找找新闻的Domains有没有特征
#===============================================================================

def save_domain_stat(fname, wfname):
    domain_stat = defaultdict(lambda: 0)
    with open(fname) as f:
        d = json.load(f)
        for url in d.values():
            s = tldextract.extract(url)
            domain = '.'.join([s.domain, s.suffix])
            domain_stat[domain] += 1
    
    sorted_domain_stat = sorted(domain_stat.items(), key=lambda k: k[1], reverse=True)
    the_whole_number = sum(each[1] for each in sorted_domain_stat)
    the_largest_number = sorted_domain_stat[0][1]
    print "the percentage of the largest number in all: ", the_largest_number / float(the_whole_number)
    
    with open(wfname, "w") as wf:
        for (domain, count) in sorted_domain_stat:
            wf.write("\t".join([domain, str(count)]) + "\n")

#===============================================================================
# 给出URL中含有"news"的百分比
#===============================================================================

def count_news(fname):
    count = 0
    with open(fname) as f:
        d = json.load(f)
        for i, url in enumerate(d.values()):
            if "news" in url:
                count += 1

    return count / float(i + 1)
        

if __name__ == "__main__":
    
    fname = "../io/urls_for_one_domain.json"
    wfname = "../io/domain_stat_for_one_domain.txt"
    save_domain_stat(fname, wfname)
    
    print "# of URLs containing 'news': ", count_news(fname) 
