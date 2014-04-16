#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: cerberus.recipes.py
Description: this program gives recipes of cerberus.
Creation: 2014-1-14
Revision: 2014-1-14
"""

import re
from cerberus import Validator
from bson.objectid import ObjectId

#===============================================================================
# cerberus是一个validation tool for Python dictionaries
# http://cerberus.readthedocs.org/en/latest/
#     1. 基本用法
#===============================================================================

schema = {'name': {'type': 'string'}}

# 第一种方式来验证schema
v = Validator(schema)

doc1 = {'name': 234}
doc2 = {'name': '234'}

print v.validate(doc1)
print v.validate(doc2)

# 第二种方式来验证schema
v1 = Validator()
print v1.validate(doc1, schema)
print v1.validate(doc2, schema)

#===============================================================================
#     2. 当出现错误时，不会中止运行或者raise an exception;而是通过errors()方法给出一系列错误
#===============================================================================

schema = {'name': {'type': 'string'}, 'age': {'type': 'integer', 'min': 10}}
document = {'name': 1337, 'age': 5}
print v.validate(document, schema)
print v.errors

#===============================================================================
#     3. setting the unknown
#     可以在schema中设置是否允许未知key的出现
#===============================================================================

# 设置不允许未知key出现
schema = {'name': {'type': 'string', 'maxlength': 10}}
print v.validate({'name': 'john', 'sex': 'M'})
print v.errors

# 设置允许未知key的出现
v.allow_unknown = True
print v.validate({'name': 'john', 'sex': 'M'})

# 初始化Validator时设置是否允许未知key的出现
v = Validator(schema=schema, allow_unknown=True)
print v.validate({'name': 'john', 'sex': 'M'})

#===============================================================================
#     4. 定制化schema中的评价metrics
#===============================================================================

class MyValidator(Validator):
    def _validate_isodd(self, isodd, field, value):
        if isodd and not bool(value & 1):
            self._error(field, "Must be an odd number")

schema = {'age': {'type': 'integer', 'isodd': True}}
doc = {'age': 5}

myValidator = MyValidator()
print myValidator.validate(doc, schema)

#===============================================================================
#     5. 增加新的数据类型（没有完全搞明白）***
#===============================================================================

# class MyValidator2(Validator):
#     def _validate_type_objectid(self, field, value):
#         if not re.match('[a-f0-9]{2}', value):
#             self._error(field, 'not ObjectId')
# 
# schema = {'age': {'type': 'objectid'}}
# doc = {'age': ObjectId("52b9e65d1d41c82558a44063")}
# 
# myValidator2 = MyValidator2()
# print myValidator.validate(doc, schema)

#===============================================================================
# Validation Rules
#     1. type自带值可以是：（也可以自定义添加数据类型）
#         string
#         integer
#         float
#         boolean
#         datetime
#         dict
#         list
#     2. 最先检验nullable,接着type checking，一旦失败，忽略其它的检验。
#     3. required, 除非调用validate()时，加上参数update=True
#     4. readonly时，表示该field不应该出现
#     5. nullable时，表示field的值可以是None
#     6. minlength, maxlength适用于string & list
#     7. min, max适用于integer
#     8. allowed适用于string, list,表示值是否在allowed列表里
#     9. empty适用于string. False表示不允许field的值为空字符串
#     10. items适用于list,定义了列表中元素类型允许的列表
#     11. schema适用于dict, list,表示schema里可以嵌套schema
#===============================================================================