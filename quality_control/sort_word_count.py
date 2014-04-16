#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: quality_control.sort_word_count.py
Description: this program
Creation: 2014-1-23
Revision: 2014-1-23
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

def sorted_word_count(ofpath):
    wfpath = ofpath + "_sorted"
    with open(wfpath, 'w') as wf:
        output = []
        with open(ofpath) as of:
            for line in of:
                new_line = line.strip().split('\t')
                output.append(new_line)
        output.sort(key=lambda k: k[1])
        
        for each in output:
            wf.write("\t".join(each) + '\n')

if __name__ == "__main__":
    ofpath = ""
    sorted_word_count(ofpath)