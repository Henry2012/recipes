#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: sundries.cmp.py
Description: this program
Creation: 2014-4-16
Revision: 2014-4-16
"""

def get_numbers(fname):
    numbers = set()
    with open(fname) as f:
        for line in f:
            numbers.add(int(line.strip()))
    return numbers

def cmp(son_fname, fname):
    son_numbers = get_numbers(son_fname)
    numbers = get_numbers(fname)
    assert son_numbers.issubset(numbers)
    difference = numbers.difference(son_numbers)
    
    with open('../EverstingDMP/io/ID_ISSUE.TXT', 'w') as wf:
        for each in difference:
            wf.write("%s\n" % each)

if __name__ == "__main__":
    son_fname, fname = ("../EverstingDMP/io/ID_IN_TELECOM_TAG_V2.TXT", "../EverstingDMP/io/ID_FOR_NOT_NULL_QUERY.TXT")
    cmp(son_fname, fname)
