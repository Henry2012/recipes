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

from util import (is_in_the_same_period_as,
                  get_media_datetime)

# def save_events_in_pkl(event_fname, event_distinction_fname,
#                     init_event_id_fname, event_category,
#                     time_period):
#     sorted_data_frame = construct_event_data_frame(event_fname, event_category)
# 
#     #===============================================================================
#     # 不同事件有不一样的时间窗口，对于具体的某一事件有固定的时间窗口
#     #     1. 将事件按照固定的时间窗口进行归类
#     #     2. time_perioed的单位是天
#     #===============================================================================
#     
#     all_period_records = split_records_into_periods(sorted_data_frame, time_period)
#     all_events = distinguish_events(all_period_records,
#                                     init_event_id_fname)
#     
#     save_cpickle(all_events, event_distinction_fname)
#     return all_events

def split_records_into_periods(sorted_data_frame, time_period):
    all_period_records = []
    one_period_records = []
    for i, (id, media_dtime, featured_fields) in enumerate(sorted_data_frame):
        if not i:
            first_dtime_in_one_period = media_dtime
            one_period_records.append((id, media_dtime, featured_fields))
        elif is_in_the_same_period_as(first_dtime_in_one_period, media_dtime, time_period):
            one_period_records.append((id, media_dtime, featured_fields))
        else:
            all_period_records.append(one_period_records)
            one_period_records = []
            one_period_records.append((id, media_dtime, featured_fields))
            first_dtime_in_one_period = media_dtime
    else:
        all_period_records.append(one_period_records)
    
    return all_period_records

def construct_event_data_frame(event_fname, event_category):
    data_frame = []
    with open(event_fname) as f:
        for i, line in enumerate(f):
            if i > 50:
                break
            
            # get detailed info
            splitted_line = line.strip().split('\t')
            id = get_id(splitted_line)
            media_dtime = get_media_datetime(id)
            featured_fields = get_featured_fields(splitted_line, event_category)
            
            # load info into data_frame
            info = []
            info.append(id)
            info.append(media_dtime)
            info.append(featured_fields)
            
            data_frame.append(info)
    
    sorted_data_frame = sorted(data_frame, key=lambda k: k[1])
    return sorted_data_frame

def get_featured_fields(splitted_line, event_category):
    '''
    featured_fields是指：通过（域值+时间）确定具体的一个事件：
        1. 比如对于stock-gain而言，（公司名+时间）就足以对事件进行first story detection
    '''
    featured_fields = []
    if event_category == 'stock-gain':
        company = splitted_line[-1]
        featured_fields.append(company)
    elif event_category == 'analyst-ratings':
        # ratee, rater
        for each in splitted_line[-2:]:
            featured_fields.append(each)
    
    return tuple(featured_fields)

def get_id(splitted_line):
    return splitted_line[0]

    