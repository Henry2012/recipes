#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: gz.recipes.py
Description: this program deals with compressing and uncompressing
Creation: 2013-11-18
Revision: 2013-11-18
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

import gzip
import os
import pdb
import tarfile

basepath = os.path.dirname(__file__)
dirpath = os.path.abspath(os.path.join(basepath, '..', 'io/'))

#===============================================================================
# 读取*.gz
#===============================================================================

# fname = "000315_0.gz"
# fpath = os.path.join(dirpath, fname)
#   
# with gzip.open(fpath) as gf:
#     for each in gf.readlines():
#         print each

#===============================================================================
# 写入*.gz
#===============================================================================

# fname = "test.gz"
# fpath = os.path.join(dirpath, fname)
#  
# with gzip.open(fpath, 'wb') as wf:
#     wf.write("record")
#     wf.write("a")

#===============================================================================
# uncompress *.tar.gz
#===============================================================================

# fname = "schedule-0.1.6.tar.gz"
# fpath = os.path.join(dirpath, fname)
#  
# tar = tarfile.open(fpath, "r:gz")
# for name in tar.getnames():
#     # dirpath gives where to uncompress files
#     tar.extract(name, dirpath)
# tar.close()

#===============================================================================
# 解压*.gz
#===============================================================================

fname = "000281_0.gz"
fpath = os.path.join(dirpath, fname)

tar = gzip.open(fpath, "rb")
for name in tar.getnames():
    # dirpath gives where to uncompress files
    tar.extract(name, dirpath)
tar.close()