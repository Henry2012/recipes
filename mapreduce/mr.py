#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: mapreduce.mr.py
Description: this program
Creation: 2014-4-17
Revision: 2014-4-17
"""

import json
import sys
from dumbo import run

reload(sys)
sys.setdefaultencoding('utf8')

class Mapper(object):
    def __init__(self):
        pass

    def __call__(self, key, value):
        record = json.loads(value.strip())
        if "city" in record:
            yield record['city'], 1

class Reducer(object):
    def __init__(self):
        pass

    def __call__(self, key, values):
        yield key, sum(values)


if __name__ == '__main__':
    run(Mapper, Reducer)
