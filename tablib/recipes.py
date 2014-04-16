#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: tablib.recipes.py
Description: this program deals with tablib
Creation: 2013-11-12
Revision: 2013-11-12
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

import tablib

headers = ('first_name', 'last_name')

data = [
    ('John', 'Adams'),
    ('George', 'Washington'),
    ('Qiqun', "Han")]

# data = tablib.Dataset(*data, headers=headers)
data = tablib.Dataset(*data)

with open('../io/people.xls', 'wb+') as f:
    f.write(data.xls)