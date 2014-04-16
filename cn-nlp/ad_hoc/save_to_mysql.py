#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: .py
Description: this program
Creation: 2014-2-20
Revision: 2014-2-20
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

import os
import pdb
import sys
basepath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(basepath, "..")))

from copy import copy
from ConfigParser import SafeConfigParser
from mysqlAPI import Mysql
from util import (load_cpickle,
                  save_cpickle,
                  get_update_sqlstr,
                  UPDATE_KEYS,
                  ALL_KEYS,
                  get_insert_and_update_sqlstr,
                  get_stock_quote_mapping,
                  update_or_insert)

parser = SafeConfigParser()
cfg_fpath = os.path.join('../', 'db.cfg')
parser.read(cfg_fpath)

host = parser.get('production', 'host')
port = parser.getint('production', 'port')
user = parser.get('production', 'user')
pwd = parser.get('production', 'pwd')
dbname = parser.get('production', 'dbname')
event_alpha_tname = 'event_alpha_for_dev_20140219_copy'
company_tname = 'company'

mysql = Mysql(host, port, user, pwd, dbname)

#===============================================================================
# 切分数据：
#     1. id只出现了一次
#     2. id出现了多次
#===============================================================================

def split_event_distinction_file(event_distinction_pkl_fname,
                                 once_pkl_fname,
                                 more_pkl_fname):
    data_info = load_cpickle(event_distinction_pkl_fname)

    once = {}
    more = {}
    for id, events in data_info.iteritems():
        if len(events) == 1:
            once[id] = events
        else:
            more[id] = events
    
    save_cpickle(once, once_pkl_fname)
    save_cpickle(more, more_pkl_fname)

def update_events(event_category):
    if event_category == 'stock-gain':
        update_stock_gain_events(once_in_stock_gain_pkl_fname,
                                 more_in_stock_gain_pkl_fname)

def update_analyst_ratings__events(analyst_ratings_event_distinction_fname):
    stock_quote_mapping = get_stock_quote_mapping(mysql, company_tname)
    
    data_info = load_cpickle(analyst_ratings_event_distinction_fname)
    
    for i, (record_id, events) in enumerate(data_info.iteritems()):
#         if i > 50:
#             break
        flag = update_or_insert(mysql, event_alpha_tname, record_id)
        print flag
        if flag == 'UPDATE':
            if len(events) == 1:
                event = events[0]
                event_id = event['event_id']
                event_novelty_score = event['story_id']
                company = event['company']
                
    #             print company
    #             print unicode(company, 'utf8')
    #             print unicode(company, 'utf8') in stock_quote_mapping
    #             pdb.set_trace()
    
                yahoo_code = stock_quote_mapping[unicode(company, 'utf8')]
                
                update_values = ['COMP', company, 'analyst-ratings', 'change', '', 'analyst-ratings-change',
                                 yahoo_code, 1, event_id, event_novelty_score]
                upd_sqlstr = get_update_sqlstr(event_alpha_tname, UPDATE_KEYS, update_values, record_id)
                mysql.execute(upd_sqlstr)
            else:
                first, others = events[0], events[1:]
                
                # 1st
                event_id = first['event_id']
                event_novelty_score = first['story_id']
                company = first['company']
                yahoo_code = stock_quote_mapping[unicode(company, 'utf8')]
                update_values = ['COMP', company, 'analyst-ratings', 'change', '', 'analyst-ratings-change',
                                 yahoo_code, 1, event_id, event_novelty_score]
                upd_sqlstr = get_update_sqlstr(event_alpha_tname, UPDATE_KEYS, update_values, record_id)
                mysql.execute(upd_sqlstr)
                
                # else
                for event in others:
                    event_id = event['event_id']
                    event_novelty_score = event['story_id']
                    company = event['company']
                    yahoo_code = stock_quote_mapping[unicode(company, 'utf8')]
                    
                    keys_in_str = ','.join(ALL_KEYS)
    
                    all_keys_copied = copy(ALL_KEYS)
                    all_keys_copied[1] = "'%s'" % company
                    all_keys_copied[6] = "'%s'" % yahoo_code
                    all_keys_copied[-3] = "'%s'" % event_id
                    all_keys_copied[-2] = "'%s'" % event_novelty_score
                    updated_keys_in_str = ','.join(all_keys_copied)
                
                    template = '''
                    insert into %s (%s)
                    select %s
                    from %s
                    where id=%s
                    '''
                
                    insert_and_upd_sqlstr = template % (event_alpha_tname, keys_in_str,
                                         updated_keys_in_str, event_alpha_tname,
                                         record_id)
                    mysql.execute(insert_and_upd_sqlstr)
        else:
            for event in events:
                event_id = event['event_id']
                event_novelty_score = event['story_id']
                company = event['company']
                yahoo_code = stock_quote_mapping[unicode(company, 'utf8')]
                
                keys_in_str = ','.join(ALL_KEYS)

                all_keys_copied = copy(ALL_KEYS)
                all_keys_copied[1] = "'%s'" % company
                all_keys_copied[6] = "'%s'" % yahoo_code
                all_keys_copied[-3] = "'%s'" % event_id
                all_keys_copied[-2] = "'%s'" % event_novelty_score
                updated_keys_in_str = ','.join(all_keys_copied)
            
                template = '''
                insert into %s (%s)
                select %s
                from %s
                where id=%s
                '''
            
                insert_and_upd_sqlstr = template % (event_alpha_tname, keys_in_str,
                                     updated_keys_in_str, event_alpha_tname,
                                     record_id)
                mysql.execute(insert_and_upd_sqlstr)
    mysql.commit()
    
def update_stock_gain_events(stock_gain_event_distinction_fname):
    stock_quote_mapping = get_stock_quote_mapping(mysql, company_tname)
    
    data_info = load_cpickle(stock_gain_event_distinction_fname)
    
    for i, (record_id, events) in enumerate(data_info.iteritems()):
#         if i > 50:
#             break
        if len(events) == 1:
            event = events[0]
            event_id = event['event_id']
            event_novelty_score = event['story_id']
            company = event['company']
            
#             print company
#             print unicode(company, 'utf8')
#             print unicode(company, 'utf8') in stock_quote_mapping
#             pdb.set_trace()

            yahoo_code = stock_quote_mapping[unicode(company, 'utf8')]
            
            update_values = ['COMP', company, 'stock-prices', 'stock', 'gain', 'stock-gain',
                             yahoo_code, 1, event_id, event_novelty_score]
            upd_sqlstr = get_update_sqlstr(event_alpha_tname, UPDATE_KEYS, update_values, record_id)
            mysql.execute(upd_sqlstr)
        else:
            first, others = events[0], events[1:]
            
            # 1st
            event_id = first['event_id']
            event_novelty_score = first['story_id']
            company = first['company']
            yahoo_code = stock_quote_mapping[unicode(company, 'utf8')]
            update_values = ['COMP', company, 'stock-prices', 'stock', 'gain', 'stock-gain',
                             yahoo_code, 1, event_id, event_novelty_score]
            upd_sqlstr = get_update_sqlstr(event_alpha_tname, UPDATE_KEYS, update_values, record_id)
            mysql.execute(upd_sqlstr)
            
            # else
            for event in others:
                event_id = event['event_id']
                event_novelty_score = event['story_id']
                company = event['company']
                yahoo_code = stock_quote_mapping[unicode(company, 'utf8')]
                
                keys_in_str = ','.join(ALL_KEYS)

                all_keys_copied = copy(ALL_KEYS)
                all_keys_copied[1] = "'%s'" % company
                all_keys_copied[6] = "'%s'" % yahoo_code
                all_keys_copied[-3] = "'%s'" % event_id
                all_keys_copied[-2] = "'%s'" % event_novelty_score
                updated_keys_in_str = ','.join(all_keys_copied)
            
                template = '''
                insert into %s (%s)
                select %s
                from %s
                where id=%s
                '''
            
                insert_and_upd_sqlstr = template % (event_alpha_tname, keys_in_str,
                                     updated_keys_in_str, event_alpha_tname,
                                     record_id)
                mysql.execute(insert_and_upd_sqlstr)
    mysql.commit()

if __name__ == "__main__":
    stock_gain_event_distinction_fname = "../io/test_v2/stock_gain_event_distinction.pkl"
    analyst_ratings_event_distinction_fname = "../io/test_v2/analyst_ratings_event_distinction.pkl"
    update_analyst_ratings__events(analyst_ratings_event_distinction_fname)
