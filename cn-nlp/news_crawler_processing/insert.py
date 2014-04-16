# -*- coding: utf-8 -*-
# Author: Peng Chao
# Copyright: EverString
# Date:
# Distributed under terms of the EverString license.

import os
import sys
basepath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(basepath, "..")))

from insert_util import insert_into_mysql_in_batch
from util import (get_mysql,
                  get_db_parser)

#===============================================================================
# 将一个文件夹里每个月的新闻文件全部导入数据库
#===============================================================================

def insert_wholly(db, concerned_dir, tname):
    counter_for_all_records = 0
    counter_for_invalid_records = 0
    all_file_size = 0
    for fname in os.listdir(concerned_dir):
        fpath = os.path.join(concerned_dir, fname)
        fsize = os.stat(fpath).st_size
    
        if not (counter_for_all_records % 1000):
            print "# records processed: ", counter_for_all_records
        
        # 注意只统计每个月的数据，也就是文件名中只有一个连字符
        if (fname.endswith('.txt') and
            "err" not in fname and
            fsize and
            len(fname.split('-')) == 2):
            #===============================================================================
            # 每一个txt文件作为输入，插入MySQL
            #===============================================================================
            (counter_for_invalid_records,
             counter_for_all_records) = insert_into_mysql_in_batch(db, fpath, tname,
                                                                   counter_for_invalid_records,
                                                                   counter_for_all_records)
    
            #===============================================================================
            # 统计值
            #===============================================================================
            all_file_size += fsize
    
    print "# all records: ", counter_for_all_records
    print "# invalid records: ", counter_for_invalid_records
    print "# size of all the above files: ", all_file_size
    db.close()

#===============================================================================
# 增量地导入每天数据
#===============================================================================

def insert_incrementally(db, fname, concerned_dir, tname):
    counter_for_all_records = 0
    counter_for_invalid_records = 0
    all_file_size = 0
    fpath = os.path.join(concerned_dir, fname)
    fsize = os.stat(fpath).st_size
    
        
    #===============================================================================
    # 1. 再检查文件名是否合法：是否含有两个连字符
    # 2. 检查文件大小是否为0
    #===============================================================================
    if (fname.endswith('.txt') and
        "err" not in fname and
        fsize and
        len(fname.split('-')) == 3):
        #===============================================================================
        # 每一个txt文件作为输入，插入MySQL
        #===============================================================================
        (counter_for_invalid_records,
         counter_for_all_records) = insert_into_mysql_in_batch(db, fpath, tname,
                                                               counter_for_invalid_records,
                                                               counter_for_all_records)

        #===============================================================================
        # 统计值
        #===============================================================================
        all_file_size += fsize
    
    print "# all records: ", counter_for_all_records
    print "# invalid records: ", counter_for_invalid_records
    print "# size of all the above files: ", all_file_size
    db.close()
    

if __name__ == "__main__":
    environ = 'local'
    PARSER = get_db_parser()
    TNAME = PARSER.get(environ, 'news_title_tname')
    DB = get_mysql(environ)
    
    #===============================================================================
    # 全量插入数据
    #===============================================================================
    #CURRENT_DIR = '/mnt/data/qiqun.h/crawler_output/crawler-2014/'
    #insert_wholly(DB, concerned_dir, TNAME)
    
    #===============================================================================
    # 增量插入数据
    #===============================================================================
    concerned_dir = 'D:/gitStuff/recipes/cn-nlp/io/crawler-2014-for-test'
    fname = '2014-3-12.txt'
    insert_incrementally(DB, fname, concerned_dir, TNAME)