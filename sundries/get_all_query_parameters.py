#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: sundries.get_all_query_parameters.py
Description: this program
Creation: 2013-12-29
Revision: 2013-12-29
"""

import json

query_parameters = []

with open("../io/referers.json") as f:
# with open("../io/test.json") as f:
    d = json.load(f)

# for k, v in d.iteritems():
#     print k, v
#     raw_input()
    
for k1, v1 in d.items():
#     if k1 != "search":
#         continue

    for k2, v2 in v1.iteritems():
#         if k2 == "Baidu":
#             print v2
        if "parameters" in v2:
            query_parameters.extend(v2["parameters"])

print set(query_parameters)