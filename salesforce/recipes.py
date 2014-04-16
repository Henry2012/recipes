#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: salesforce.recipes.py
Description: this program
Creation: 2013-12-10
Revision: 2013-12-10
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

error_domains = []
with open("../io/erroneous_domains.txt") as f1:
    for line in f1:
        error_domains.append(line.strip())

all_domains = []
with open("../io/salesforce_domains_with_no_founding_date.txt") as f2:
    for line in f2:
        all_domains.append(line.strip())
        
with open("../io/salesforce_domains_with_no_founding_date_plus_flagged.txt", "w") as f3:
    for d in all_domains:
        if d in error_domains:
            f3.write(d + "\t" + "error" + "\n")
        else:
            f3.write(d + "\t" + "\n")
