#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: sundries.read_dict_from_json.py
Description: this program reads a dict from a json file.
Creation: 2014-1-7
Revision: 2014-1-7
"""

import json

def read_dict(fname):
    titles = []
    with open(fname) as f:
        a_dict = json.load(f)
        for title in a_dict.values():
            titles.append(title)
    return titles

if __name__ == "__main__":
    
    fname = "../io/job_titles.json"
    
    titles = read_dict(fname)
    
    with open("../io/job_titls_without_lineno.txt", "w") as wf:
        for title in titles:
            if not title:
                continue
            wf.write(title + "\n")