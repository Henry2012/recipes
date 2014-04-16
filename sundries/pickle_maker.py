#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: sundries.pickle_maker.py
Description: this program
Creation: 2014-2-9
Revision: 2014-2-9
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

import os
import pickle
import pdb

def save_pickle(data_info, output_source):
    with open(output_source, 'wb') as wf:
        pickle.dump(data_info, wf)

def flatten_fnames(root, new_root):
    fnames = {}
    for fname in os.listdir(root):
        absolute_fname = os.path.realpath(os.path.join(root, fname))
        new_absolute_fname = os.path.realpath(os.path.join(new_root, fname.strip('.txt') + '.pkl'))
        #print absolute_fname, new_absolute_fname
        fnames[absolute_fname] = new_absolute_fname

    return fnames

def transfer_to_pickle_for_all(root, new_root):
    fnames = flatten_fnames(root, new_root)
    #pdb.set_trace()
    for fname, new_fname in fnames.iteritems():
        #print fname, new_fname
        with open(fname) as f:
            info = eval(f.read())
            #print info
            save_pickle(info, new_fname)

if __name__ == "__main__":
#     root = '/media/ebs1/pc/unzip/'
#     new_root = '/media/ebs1/pc/industry_models_in_pickle/'

    root = '../io/test/'
    new_root = '../io/new_test/'
    transfer_to_pickle_for_all(root, new_root)
