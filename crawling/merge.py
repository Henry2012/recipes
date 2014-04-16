#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: crawling.merge.py
Description: this program
Creation: 2013-11-29
Revision: 2013-11-29
"""

import tldextract
import pdb

prefix = "https://appexchange.salesforce.com"

# all = []
# with open("../io/result2.txt") as f:
#    
#     for line in f:
#         url_part, name = line.strip().split("    ")
#         url = prefix + url_part
#         all.append([url, name])
# 
# extracted = []
# with open("../io/name_domain.txt") as f2:
#     for line2 in f2:
#         name2, url2 = line2.strip().split("\t")
#         s = tldextract.extract(url2)
#         domain_name = '.'.join([s.domain, s.suffix])
#         extracted.append([domain_name, name2])
# 
# pdb.set_trace()
# 
# with open('../io/merged.txt', 'w') as wf:
#     for url, name in all:
#         for domain, name2 in extracted:
#             if name == name2:
#                 wf.write("%s\t%s\t%s\n" % (url, name, domain))
#                 break
#         else:
#             wf.write("%s\t%s\n" % (url, name))

with open("../io/missing_domain.txt") as f:
    for line in f:
        url = line.strip()
        s = tldextract.extract(url)
        domain_name = '.'.join([s.domain, s.suffix])
        print domain_name