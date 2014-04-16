#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: json.recipes.py
Description: this program play around json library.
Creation: 2013-12-13
Revision: 2013-12-13
"""

import pdb

#===============================================================================
# 1. 主要研究了写入json的数据格式：将dict写入json时，keys必须是string
# 2. dumps & dump|loads & load的不同：
#    loads接收string or buffer，load接收file instance;
#    loads可以理解成load string 
#===============================================================================

import json

#===============================================================================
# 再现使用写入json时可能出现的错误：
# 1. dump & dumps不同
# 2. 字典写入时，keys的类型必须是string
#===============================================================================

# d = {("a", "b"): 1,
#      ("a", "c"): 1}
# 
# with open("../io/test.txt", "w") as wf:
#     # TypeError: dump() takes at least 2 arguments (1 given)
# #     wf.write(json.dump(d))
#      
#     # TypeError: keys must be a string
#     wf.write(json.dumps(d))

#===============================================================================
# 换写入数据
# 仍然报错：TypeError: keys must be a string
#===============================================================================

# d = {1: "a",
#      2: "b"}
# 
# with open("../io/test.txt", "w") as wf:
#     wf.write(json.dumps(d))

#===============================================================================
# 写入json:正确的数据格式
#===============================================================================

# d = {"a": 1,
#      "b": 2}
d = [1, 2.0, 3]
  
with open("../io/test.txt", "w") as wf:
    wf.write(json.dumps(d))

with open('../io/test.txt') as f:
    data = json.load(f)

pdb.set_trace()

#===============================================================================
# 读取json格式的文件，使用loads or load
#===============================================================================

with open("../io/test.json") as f:
    d = json.load(f)
    for k, v in d.iteritems():
        print k, v