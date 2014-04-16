#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: pickle.recipes.py
Description: this program
Creation: 2014-2-10
Revision: 2014-2-10
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

import pickle
import cPickle

#this function saves a pickle file
def save_pickle(data_info, output_source):
    with open(output_source, 'wb') as wf:
        pickle.dump(data_info, wf)
        
def load_pickle(fname):
    with open(fname, 'rb') as rf:
        output = pickle.load(rf)
    return output

def save_cpickle(data_info, output_source):
    with open(output_source, 'wb') as wf:
        cPickle.dump(data_info, wf, -1)

def load_cpickle(fname):
    with open(fname, 'rb') as rf:
        output = cPickle.load(rf)
    return output

if __name__ == "__main__":
    fname = '../io/new_test/10.pkl'
    output = load_pickle(fname)
    print len(output), type(output)