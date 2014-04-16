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
import re
import sys
basepath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(basepath, "..")))

from collections import defaultdict
from file_names import (colon_with_more_quotes_with_hyphen_with_all_quotes_in_front_fname,
                        colon_with_one_quote_without_zhengquan_before_colon_with_hyphen_between_hyphen_and_colon_fname,
                        analyst_ratings_fname,
                        analyst_ratings_event_distinction_fname,
                        init_event_id_fname)
from util import (get_media_datetime,
                  is_in_the_same_day_as,
                  save_cpickle,
                  load_cpickle,
                  get_init_event_id,
                  update_init_event_id)

def main(analyst_ratings_fname, analyst_ratings_event_distinction_fname,
         init_event_id_fname):
    sorted_data_frame = construct_analyst_ratings_data_frame(analyst_ratings_fname)
    all_day_records = split_records_into_days(sorted_data_frame)
    all_events = distinguish_events(all_day_records,
                                    init_event_id_fname)
    
    save_cpickle(all_events, analyst_ratings_event_distinction_fname)
    return all_events

def distinguish_events(all_day_records,
                       init_event_id_fname):
    '''
    all_events的存储形式：
    {'23243':{'event_id': 0,
              'story_id': 1},
              'company': ''}
    '''
    init_event_id = get_init_event_id(init_event_id_fname)
    all_events = defaultdict(list)
    for one_day_records in all_day_records:
        events = defaultdict(list)
        for (id, ratee, rater, media_dtime) in one_day_records:
            if ">|<" in rater:
                splitted_raters = rater.split(">|<")
                for rater in splitted_raters:
                    events[(ratee, rater)].append(id)
            else:
                events[(ratee, rater)].append(id)
        
#         pprint(events)
#         pdb.set_trace()
        
        for (_, rater), ids in events.iteritems():
            story_id = 0
            for i, id in enumerate(ids):
                all_events[int(id)].append({'event_id': init_event_id,
                                  'story_id': story_id,
                                  'company': rater})
                story_id += 1
            
            init_event_id += 1
        
#         pprint(dict(all_events))
#         pdb.set_trace()
        
    update_init_event_id(init_event_id, init_event_id_fname)
    
    return dict(all_events)

def split_records_into_days(sorted_data_frame):
    all_day_records = []
    one_day_records = []
    for i, (id, ratee, raters, media_dtime) in enumerate(sorted_data_frame):
        if not i:
            first_dtime_in_one_day = media_dtime
            one_day_records.append((id, ratee, raters, media_dtime))
        elif is_in_the_same_day_as(first_dtime_in_one_day, media_dtime):
            one_day_records.append((id, ratee, raters, media_dtime))
        else:
            all_day_records.append(one_day_records)
            one_day_records = []
            one_day_records.append((id, ratee, raters, media_dtime))
            first_dtime_in_one_day = media_dtime
    else:
        all_day_records.append(one_day_records)
    
    return all_day_records

def construct_analyst_ratings_data_frame(analyst_ratings_fname):
    data_frame = []
    with open(analyst_ratings_fname) as f:
        for i, line in enumerate(f):
#             if i > 10:
#                 break
            
            id, title, ratee, raters = line.strip().split('\t')
            
            media_dtime = get_media_datetime(id)
            
            data_frame.append((id, ratee, raters, media_dtime))
    
    sorted_data_frame = sorted(data_frame, key=lambda k: k[-1])
    return sorted_data_frame

#===============================================================================
# 当前只标明这是机构评级，并提取出
#     1. 被评级的公司名（被评级的公司名可以有多个，用>|<分隔）
# 使用两个文件：
#     1. records_with_colon_with_more_quotes_with_hyphen_with_all_quotes_in_front
#     2. records_with_colon_with_one_quote_without_zhengquan_before_colon_with_hyphen_between_hyphen_and_colon
#===============================================================================

def construct_analyst_ratings_raw_file(analyst_ratings_fname,
                              colon_with_one_quote_without_zhengquan_before_colon_with_hyphen_between_hyphen_and_colon_fname,
                              colon_with_more_quotes_with_hyphen_with_all_quotes_in_front_fname):
    with open(analyst_ratings_fname, 'w') as wf:
        with open(colon_with_one_quote_without_zhengquan_before_colon_with_hyphen_between_hyphen_and_colon_fname) as f1:
            for line in f1:
                id, title, rater = line.strip().split('\t')
                ratee = title.split('-', 1)[0]
                
                # for test
#                 if len(ratee) < 4:
#                     print title, rater, ratee

                new_line = [id, title, ratee, rater]
                new_line = '\t'.join(new_line) + '\n'
                wf.write(new_line)
        
        with open(colon_with_more_quotes_with_hyphen_with_all_quotes_in_front_fname) as f2:
            for line in f2:
                id, title, companies = line.strip().split('\t')
                ratee, raters = extract_rater_and_ratee(title, companies)
                raters_in_str = ">|<".join(raters)

                new_line = [id, title, ratee, raters_in_str]
                new_line = '\t'.join(new_line) + '\n'
                wf.write(new_line)

def extract_rater_and_ratee(sent, companies):
    #===============================================================================
    # 获得被评价公司，必须在我们的公司名库里
    #===============================================================================
    
    companies = companies.split('>|<')
    comp_indexes = []

    assert len(companies) > 1
    for comp in companies:
        idx = sent.index(comp)
        comp_indexes.append((comp, idx))
        
    raters = [comp for comp, _ in sorted(comp_indexes, key=lambda k: k[-1])[1:]]

    #===============================================================================
    # 获得评级公司，不一定在我们公司名库里
    #===============================================================================
    
    ratee = sent.split('-', 1)[0]
    return ratee, raters


if __name__ == "__main__":
#     sent = "华泰证券-兴业银行-季报点评：业绩维持高增长,未来关注同业监"
#     print extract_rated_comp(sent, "华泰证券>|<兴业银行")

    #===============================================================================
    # 处理成初始事件
    #===============================================================================

#     construct_analyst_ratings_raw_file(analyst_ratings_fname,
#          colon_with_one_quote_without_zhengquan_before_colon_with_hyphen_between_hyphen_and_colon_fname,
#          colon_with_more_quotes_with_hyphen_with_all_quotes_in_front_fname)

    #===============================================================================
    # 加上event_id & story_id
    #===============================================================================
    
    main(analyst_ratings_fname, analyst_ratings_event_distinction_fname,
         init_event_id_fname)