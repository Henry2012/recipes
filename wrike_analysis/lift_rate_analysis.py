#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: wrike_news_stat.lift_rate_analysis.py
Description: this program creates lift rates for email domains based on suffixes.
Creation: 2014-1-6
Revision: 2014-1-6
"""

from collections import defaultdict

lift_rates = defaultdict(lambda: [0] * 2)

with open("../io/wrike_paid_and_suffix.txt") as f:
    for line in f:
        splitted = line.rstrip("\n").split("\t")
        paid = splitted[0]
        suffix = splitted[1]
        
        lift_rates[suffix][0] += 1
        if paid:
            lift_rates[suffix][1] += 1

with open("../io/wrike_lift_rate_for_email_suffixes.txt", "w") as wf:
    for suffix, count_list in lift_rates.iteritems():
        count_str = "\t".join(str(each) for each in count_list)
        wf.write("\t".join([suffix, count_str]) + '\n')