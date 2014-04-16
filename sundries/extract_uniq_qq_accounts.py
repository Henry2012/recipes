#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: sundries.extract_uniq_qq_accounts.py
Description: this program
Creation: 2014-4-9
Revision: 2014-4-9
"""

with open('../EverstingDMP/io/result.txt') as f1:
    with open('../EverstingDMP/io/uniq_qq_accounts.txt', 'w') as wf1:
        qq = set()
        for line in f1:
            for each in line.strip().split("\t")[-1].split("|"):
                if each:
                    qq.add(each)
        
        for each in list(qq):
            wf1.write(each + "\n")