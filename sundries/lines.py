#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: sundries.lines.py
Creation: 2014-1-8
Revision: 2014-1-8
"""

# with open("../io/PEPL_AShrIndependentDirector_updated.txt", "w") as wf:
#     with open("../io/PEPL_AShrIndependentDirector.txt") as f:
#         for line in f:
#             for each in line.strip().split(","):
#                 wf.write(each + "\n")

with open("../io/CPUS_HuaXunFinance_updated.txt", "w") as wf:
    with open("../io/CPUS_HuaXunFinance_v2.txt") as f:
        for line in f:
            for each in line.strip().split(" "):
                wf.write(each + "\n")