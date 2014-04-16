#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: read_pickle.py
Description: this program
Creation: 2013-12-4
Revision: 2013-12-4
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

import cPickle
import pdb

fname = "io/es_html_network_signals_11_15_2013.pkl"
with open(fname) as f:
    d = cPickle.load(f)

for k, v in d.iteritems():
    print k, v

pdb.set_trace()
