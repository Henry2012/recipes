#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: .py
Description: this program
Creation: 2014-2-18
Revision: 2014-2-18
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

import os
import pdb
import sys
basepath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(basepath, "..")))

from collections import defaultdict
from event_distinction_util import (split_records_into_periods,
                                    construct_event_data_frame)
from file_names import (init_event_id_fname,
                        stock_gain_fname,
                        stock_gain_event_distinction_fname)
from util import (save_cpickle,
                  load_cpickle,
                  get_init_event_id,
                  update_init_event_id)

#===============================================================================
# 这是利用event_distinction_util对stock-gain事件进行处理
# 最后的结果和event_distinction_for_stock_gain一样
#===============================================================================

def main(stock_gain_fname, stock_gain_event_distinction_fname,
         init_event_id_fname, time_period=1):
    sorted_data_frame = construct_event_data_frame(stock_gain_fname, 'stock-gain')
    all_period_records = split_records_into_periods(sorted_data_frame, time_period)
    all_events = distinguish_events(all_period_records,
                                    init_event_id_fname)
    
    save_cpickle(all_events, stock_gain_event_distinction_fname)
    return all_events

def distinguish_events(all_period_records,
                       init_event_id_fname):
    '''
    all_events的存储形式：
    {23243:{'event_id': 0,
              'story_id': 1},
              'company': ''}
    '''
    init_event_id = get_init_event_id(init_event_id_fname)
    all_events = defaultdict(list)
    for one_period_records in all_period_records:
        events = defaultdict(list)
        for (id, media_dtime, featured_fields) in one_period_records:
            company = featured_fields[0]
            if ">|<" in company:
                companies = company.split(">|<")
                for company in companies:
                    events[company].append(id)
            else:
                events[company].append(id)
        
#         pprint(events)
#         pdb.set_trace()
        
        for company, ids in events.iteritems():
            story_id = 0
            for i, id in enumerate(ids):
                all_events[int(id)].append({'event_id': init_event_id,
                                  'story_id': story_id,
                                  'company': company})
                story_id += 1
            
            init_event_id += 1
        
#         pprint(dict(all_events))
#         pdb.set_trace()
        
    update_init_event_id(init_event_id, init_event_id_fname)
    
    return dict(all_events)

if __name__ == "__main__":
    main(stock_gain_fname, stock_gain_event_distinction_fname,
         init_event_id_fname, time_period=1)