#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: .py
Description: this program
Creation: 2014-2-17
Revision: 2014-2-17
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

import os
import pdb
import sys
basepath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(basepath, "..")))

from collections import defaultdict
from pprint import pprint
from file_names import (init_event_id_fname,
                        stock_gain_fname,
                        stock_gain_event_distinction_fname)
from util import (get_media_datetime,
                  is_in_the_same_day_as,
                  save_cpickle,
                  load_cpickle,
                  get_init_event_id,
                  update_init_event_id)

#===============================================================================
# stock-gain
#===============================================================================

def main(stock_gain_fname, stock_gain_event_distinction_fname,
         init_event_id_fname):
    sorted_data_frame = construct_stock_gain_data_frame(stock_gain_fname)
    all_day_records = split_records_into_days(sorted_data_frame)
    all_events = distinguish_events(all_day_records,
                                    init_event_id_fname)
    
    save_cpickle(all_events, stock_gain_event_distinction_fname)
    return all_events

def distinguish_events(all_day_records,
                       init_event_id_fname):
    '''
    all_events的存储形式：
    {23243:{'event_id': 0,
              'story_id': 1},
              'company': ''}
    '''
    init_event_id = get_init_event_id(init_event_id_fname)
    all_events = defaultdict(list)
    for one_day_records in all_day_records:
        events = defaultdict(list)
        for (id, company, media_dtime) in one_day_records:
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

def split_records_into_days(sorted_data_frame):
    all_day_records = []
    one_day_records = []
    for i, (id, company, media_dtime) in enumerate(sorted_data_frame):
        if not i:
            first_dtime_in_one_day = media_dtime
            one_day_records.append((id, company, media_dtime))
        elif is_in_the_same_day_as(first_dtime_in_one_day, media_dtime):
            one_day_records.append((id, company, media_dtime))
        else:
            all_day_records.append(one_day_records)
            one_day_records = []
            one_day_records.append((id, company, media_dtime))
            first_dtime_in_one_day = media_dtime
    else:
        all_day_records.append(one_day_records)
    
    return all_day_records

def construct_stock_gain_data_frame(stock_gain_fname):
    data_frame = []
    with open(stock_gain_fname) as f:
        for i, line in enumerate(f):
#             if i > 50:
#                 break
            id, title, company = line.strip().split('\t')
            
            media_dtime = get_media_datetime(id)
            
            data_frame.append((id, company, media_dtime))
    
    sorted_data_frame = sorted(data_frame, key=lambda k: k[-1])
    return sorted_data_framezzzzz

if __name__ == "__main__":
#     print [get_init_event_id()]

    all_events = main(stock_gain_fname,
                      stock_gain_event_distinction_fname,
                       init_event_id_fname)

    # load pkl
#     all_events = load_cpickle(stock_gain_event_distinction_fname,
#                               init_event_id_fname)

    #pdb.set_trace()
