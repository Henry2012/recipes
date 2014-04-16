#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: os.recipes.py
Description: this program deals with os package
Creation: 2013-11-10
Revision: 2013-11-10
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

import os
import pdb
import sys

#===============================================================================
# Shell 接受参数
# python foo.py arg1中sys.argv[0]指的是foo.py
#===============================================================================

# sys.argv[1]

#===============================================================================
# 从相对路径中import libraries
# 【注意点】
#     1. os.path.join()只不过是字符串的join，需要用abspath方法生成通常意义上的路径
#     2. 举例来说，下面代码join的结果是"D:\gitStuff\recipes\os_and_sys\..";利用abspath之后才是"D:\gitStuff\recipes"
#     3. open函数能够与"D:\gitStuff\recipes\os_and_sys\.."这样格式类似的文本路径，不需要再用abspath
#===============================================================================

# 通过如下方式可以import该文件上层目录的模块
basepath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(basepath, "..")))

# fpath = os.path.join(basepath, "..", "io", "_test.txt")
fpath = os.path.join(basepath, "../io", "test.cfg")

with open(fpath) as f:
    print f.read()

#===============================================================================
# realpath返回真实路径
# basename返回文件名
# isfile
# isdir
# islink
# isabs返回是否为绝对路径
# sameopenfile/samefile: only available in Unix
#===============================================================================

#assert os.path.realpath(__file__) == "D:\\gitStuff\\recipes\\os\\recipes.py"

#===============================================================================
# Display the path of the directory of the current file
#===============================================================================

#assert os.path.dirname(__file__) == "D:\\gitStuff\\recipes\\os"

#===============================================================================
# abspath返回绝对路径
# 使用".."返回至上一层目录
#===============================================================================

basepath = os.path.dirname(__file__)
filepath = os.path.abspath(os.path.join(basepath, "..", 're/recipes.py'))
assert filepath == 'D:\\gitStuff\\recipes\\re\\recipes.py'

#===============================================================================
# 获得一个文件夹里所有文件的绝对路径
# dir/
#     fname_0, fname_1, ...
#===============================================================================

def flatten_fnames(root):
    fnames = []
    for fname in os.listdir(root):
        absolute_fname = os.path.realpath(os.path.join(root, fname))
        fnames.append(absolute_fname)

    return fnames

#===============================================================================
# 获得一个文件夹里所有文件的绝对路径
# dir/
#     sub_dir_0/
#         fname_0, fname_1, ...
#     sub_dir_1/
#         fname_0, fname_1, ...
#===============================================================================

def flatten_deep_fnames(root):
    final_fnames = []
    for dir_name in os.listdir(root):
        #pdb.set_trace()
        fnames = os.listdir(os.path.join(root, dir_name))
        for fname in fnames:
            #pdb.set_trace()
            final_fnames.append(os.path.join(root, dir_name, fname))
    return final_fnames

#===============================================================================
# 1. 检查某个dir是否存在于某个路径下
# 2. 若不存在，则创建该dir
#===============================================================================

print os.path.isdir("../io")
print os.path.exists("../io/test.txt")

# 创建目录
# 实现mkdir -p
if not os.path.exists("../io/test/sub_test3/"):
    os.makedirs("../io/test/sub_test3/")

#===============================================================================
# os.walk
#===============================================================================

#===============================================================================
# How to get the size of a file
#===============================================================================

print os.path.getsize('../io/titles.txt')
print os.stat('../io/titles.txt').st_size

#===============================================================================
# 计算一个文件的大小
#===============================================================================

# fpath = 'test.txt'
# print os.stat(fpath).st_size

#===============================================================================
# 计算一个文件夹下大小为0的文件个数
#===============================================================================

def count_zero_files(dir_name):
    count = 0
    for each in os.listdir(dir_name):
        fpath = os.path.join(dir_name, each)
        if (os.path.isfile(fpath) and
            not os.stat(fpath).st_size):
            count += 1
    return count

if __name__ == "__main__":
    
    print count_zero_files("../io")
