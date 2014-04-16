# -*- coding: utf-8 -*-
# Author: Peng Chao
# Copyright: EverString
# Date:
# Distributed under terms of the EverString license.

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
