# -*- coding: utf-8 -*-
# Author: Qiqun Han
# Copyright: EverString
# Date:
# Distributed under terms of the EverString license.

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import datetime
import pytz
basepath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(basepath, "..")))

from pytz import timezone
from mysqlAPI import Mysql
from util import transfer_local_dtime_str_to_utc_dtime_str

def insert_into_mysql_one_by_one(db, fpath, tname):

    with open(fpath, 'r') as f:
        for line in f:
            data_dict = {}
            elems = line.split('>|<')
            if elems[5] is None:
                continue
            sql = "select count(*) from %s where source = '" % tname + elems[5].rstrip() +"'"
            count = int(db.findOne(sql)[0])
            print count
            if count > 0:
                continue
            if elems[2] is not None:
                data_dict['title'] = elems[2].rstrip()
            if elems[4] is not None:
                data_dict['abstract'] = elems[4].rstrip()
            if elems[5] is not None:
                data_dict['source'] = elems[5].rstrip()
            if elems[1] is not None:

                #===============================================================================
                # 将本地时间转换成UTC时区的时间
                #===============================================================================
                media_date = elems[1].rstrip()
                meida_date = transfer_local_dtime_str_to_utc_dtime_str(media_date)
                data_dict['media_date'] = meida_date

            db.insert_record(data_dict, tname)
    db.commit()
    db.close()

def insert_into_mysql_in_batch(db, fpath, tname,
                               counter_for_invalid_records,
                               counter_for_all_records):
    insert_keys = ['title', 'abstract', 'source', 'media_date']
    insert_value_package = []
    with open(fpath, 'r') as f:
        for i, line in enumerate(f):
            line = line.strip()
            if line:
                elems = line.split('>|<')

                #===============================================================================
                # 将本地时间转换成UTC时区的时间
                #===============================================================================
                media_date = elems[1]
                meida_date = transfer_local_dtime_str_to_utc_dtime_str(media_date)

                if media_date and elems[2] and elems[5]:
                    source = elems[5].strip()
                    insert_value_package.append([elems[2], elems[4], source, elems[1]])
                    counter_for_all_records += 1
                else:
                    counter_for_invalid_records += 1

    db.insert_records(insert_keys, insert_value_package, tname)
    db.commit()
    return counter_for_invalid_records, counter_for_all_records
