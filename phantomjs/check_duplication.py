#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: phantomjs.check_duplication.py
Description: this program
Creation: 2013-12-5
Revision: 2013-12-5
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

import os
import pdb

def get_all_fnames(dir_name):
    fnames = set([])
    for each in os.listdir(dir_name):
        fnames.add(os.path.basename(each))
    
    return fnames

def get_all_fnames_v2(of_name):
    domains = set([])
    with open(of_name) as f:
        for line in f:
            line = line.strip()
            if line:
                if (line.endswith(".jpg") or
                    line.endswith(".png")):
                    domain = line[:-4]
                else:
                    domain = line
                domains.add(domain)

    return domains

if __name__ == "__main__":
    #===============================================================================
    # 统计我本机上的网站首页截图
    #===============================================================================
#     dir_name = "E:\screen_capturing"
#     fnames = get_all_fnames(dir_name)
#         
#     with open("../io/screenshotted_photos_mypc_v2.txt", "w") as wf:
#         for each in fnames:
#             wf.write(each + "\n")
#       
#     pdb.set_trace()
    
    #===============================================================================
    # 1. 统计所有已经获得的网站首页截图
    # 2. 对上一部获得的结果取补集
    #===============================================================================
#     of_name_orginal = "../io/3k_company_websites_and_domains.txt"
#     of_name1 = "../io/screenshotted_photos_mypc_v2.txt"
#     of_name2 = "../io/screenshotted_photos_azure_v3.txt"
#     set1 = get_all_fnames_v2(of_name1)
#     set2 = get_all_fnames_v2(of_name2)
#     set_all = set1.union(set2)
    
#     with open("../io/screenshotted_photos_both.txt", 'w') as wf:
#         for each in set_all:
#             wf.write(each + "\n")
#     pdb.set_trace()

#     with open(of_name_orginal) as f:
#         records = []
#         for line in f:
#             website, domain = line.strip().split("\t")
#             records.append([domain, website])
#         records = dict(records)
#     
#     set_difference = set_all - set(records.keys())
#     print set_difference
#     #pdb.set_trace()
#     #assert set_all.issubset(records.keys())
#     with open("../io/screenshotted_missing_domains_v3.txt", 'w') as wf:
#         for each in list(set(records.keys()) - set_all):
#             wf.write(records[each] + "\t" + each + "\n")
        
#     pdb.set_trace()

    #===============================================================================
    # Get the complementary set from 2 text files
    #===============================================================================
    bigger_fname = "../io/screenshotted_missing_domains_v3.txt"
    smaller_fname = "../io/screenshotted_photos_bigmine_v1.txt"
    
    bigger = set()
    with open(bigger_fname) as f1:
        for line in f1:
            bigger.add(line.strip().split("\t")[1])
            
    smaller = set()
    with open(smaller_fname) as f2:
        for line in f2:
            smaller.add(line.strip()[:-4])
            
    rest = bigger - smaller
    with open("../io/screenshotted_erroneous_phantomjs.txt", "w") as wf:
        for each in rest:
            wf.write("http://www." + each + "\t" + each + "\n")