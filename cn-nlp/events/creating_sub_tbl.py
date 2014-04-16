#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
Creation: 2014-3-14
Revision: 2014-3-14
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

#===============================================================================
# 根据“收购”和“并购”两个关键字提取出记录，并存储到新的表中
# 全量表：news_preprocessing_daily
# 导出后的表：stock_news_for_acqu
#===============================================================================

import os
import re
import sys
from sqlite3.test.transactions import get_db_path
basepath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(basepath, "..")))

import pdb
from util import (get_mysql,
                  get_db_parser,
                  get_all_fields)

#===============================================================================
# 从一个大的表中抽取一部分作为新的表
#     1. 利用is_extracted定义抽取的逻辑
#     2. 创建新表，与原有的表具有相同的表结构（使用navicat）
#     3. 利用create_sub_table插入满足条件的新闻
# 从news_preprocessing_daily中抽取新闻标题中含有“收购”或者“并购”的记录
#===============================================================================

def is_extracted(title):
    flag = False
    
    # 收购事件
#     if "收购" in title or "并购" in title:
#         flag = True

    # 百分号事件,从属于earnings事件
    #pattern = r'([0-9]+%-[0-9]+%)'
    #pattern = r'([0-9\.]+%-+[0-9\.]+%)'
    pattern = u'业绩|净利|盈利|利润|营收|收入'
    
    # 信用评级事件
    # 包含有连字符，可不是出现在类似于“20%-30%”的模式中
    #pattern = re.compile(r'([0-9\.]+%-+[0-9\.]+%)')
    
    if re.search(pattern, title):
        flag = True
    return flag

def create_sub_table(mysql, big_tname, small_tname):
    all_fields_in_big_tbl = ','.join(get_all_fields(mysql, big_tname))
    insert_sqlstr_fmt = '''
    insert into %s (%s)
    select %s
    from %s
    where id=%d;
    '''
    count_of_sql_exe = 0
    
    # 收购事件
    #find_sqlstr = 'select * from %s where no_of_quotes > 0' % big_tname
    
    # 百分号事件
    find_sqlstr = 'select * from %s where no_of_quotes > 0 and contains_hyphen=1' % big_tname
    
    # 信用评级事件
    #find_sqlstr = 'select * from %s where no_of_quotes > 0 and contains_hyphen=1' % big_tname
    
    for record in mysql.find(find_sqlstr):
        id = record[0]
        title = record[4]
#         print title
#         pdb.set_trace()
        if count_of_sql_exe and not (count_of_sql_exe % 1000):
            mysql.commit()
        if is_extracted(title):
            count_of_sql_exe += 1
            insert_sqlstr = insert_sqlstr_fmt % (small_tname, all_fields_in_big_tbl,
                                                 all_fields_in_big_tbl, big_tname, id)
#             print insert_sqlstr
#             break
            mysql.execute(insert_sqlstr)
    else:
        mysql.commit()
     
#===============================================================================
# 对acqu_binggou中的新闻增加一列title_dep
#===============================================================================

def expand_title_dep(mysql, ofname, wfname):
    with open(fname) as f:
        with open(wfname, 'w') as wf:
            for i, line in enumerate(f):
                if i and not (i % 100):
                    print i
                id = line.strip().split('\t')[0]
                
                #===============================================================================
                # 去除之后的\r或者\n
                #===============================================================================
                new_line = "\t".join([str(each).strip() for each in get_detailed_titles(mysql, id)]) + '\n'
                wf.write(new_line)

def get_detailed_titles(mysql, id):
    '''
    1. 根据id从stock_news_for_acqu中提取title,title_seg,title_pos,title_dep
    '''
    sqlstr_fmt = 'select id,title,title_seg,title_pos,title_dep from %s where id=%s'
    sqlstr = sqlstr_fmt % (acqu_tname, str(id))
    return mysql.find(sqlstr)[0]

if __name__ == "__main__":
    environ = 'local'
    # remote_mysql = get_mysql('production')
    local_mysql = get_mysql(environ)
    parser = get_db_parser()
    all_tname = parser.get(environ, 'news_title_tname')
    acqu_tname = 'stock_news_for_acqu'
    percentage_tname = 'stock_news_for_percentage'
    earnings_tname = 'stock_news_for_earnings'
    ratings_tname = 'stock_news_for_ratings'
    
#     fname = '../io/test_v3/acqu_binggou.txt'
#     wfname = '../io/test_v3/acqu_binggou_expanded.txt'
#     expand_title_dep(local_mysql, fname, wfname)
    
#     create_sub_table(local_mysql, all_tname, percentage_tname)
    
    title = u'江南红箭预计去年亏损800-1200万元'
    print is_extracted(title)
    local_mysql.close()
