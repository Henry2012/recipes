# -*- coding: utf-8 -*-
# Author: Peng Zhuo
# Copyright: EverString
# Date:
# Distributed under terms of the EverString license.

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from mysqlAPI import Mysql
from file_system import get_merged_fpath

def insert_into_mysql(current_dir, concerned_date):
    fpath = get_merged_fpath(current_dir, concerned_date)
    
    host = 'esdev-mysql.cloudapp.net'
    port = 3306
    user = 'esapp'
    pwd = 'esapp1'
    dbname = 'mscndemo'
    db = Mysql(host, port, user, pwd, dbname)

    with open(fpath, 'r') as f:
        for line in f:
            data_dict = {}
            elems = line.split('>|<')
            if elems[5] is None:
                continue
            sql = "select count(*) from news where source = '" + elems[5].rstrip('\r').rstrip('\t').rstrip('\n') +"'"
            count = int(db.findOne(sql)[0])
            print count
            if count > 0:
                continue
            if elems[2] is not None:
                data_dict['title'] = elems[2].rstrip('\r').rstrip('\t').rstrip('\n')
            if elems[4] is not None:
                data_dict['abstract'] = elems[4].rstrip('\r').rstrip('\t').rstrip('\n')
            if elems[5] is not None:
                data_dict['source'] = elems[5].rstrip('\r').rstrip('\t').rstrip('\n')
            if elems[1] is not None:
                data_dict['publish_date'] = elems[1].rstrip('\r').rstrip('\t').rstrip('\n')
            db.insert_record(data_dict, 'news')
    db.commit()
    db.close()
