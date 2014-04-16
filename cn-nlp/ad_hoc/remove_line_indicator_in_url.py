#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: .py
Description: this program
Creation: 2014-2-17
Revision: 2014-2-17
"""

def remove_line_indicator(old_fname, new_fname):
    with open(old_fname) as f:
        with open(new_fname, 'w') as wf:
            f = f.readlines()
            for i, line in enumerate(f):
#                 if not (i % 2):
#                     new_line = line.strip() + f[i + 1]
#                     wf.write(new_line)
                if line != "\n":
                    wf.write(line)

if __name__ == "__main__":
    old_fname = '../io/test_v2/event_alpha_for_prod_20140208_v3.txt'
    new_fname = '../io/test_v2/event_alpha_for_prod_20140208_v3_revised.txt'
    remove_line_indicator(old_fname, new_fname)