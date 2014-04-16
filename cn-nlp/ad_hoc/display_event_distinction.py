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

# from file_names import (analyst_ratings_event_distinction_fname,
#                         stock_gain_event_distinction_fname)
from util import (load_cpickle,
                  get_title)

#===============================================================================
# for print
#===============================================================================

def display(pkl_fname, txt_fname):
    '''
    all_events的存储形式：
    {'23243':[{'event_id': 0,
              'story_id': 1},
              'company': ''},...]}
    '''
    all_events = load_cpickle(pkl_fname)
    with open(txt_fname, 'w') as wf:
        for id, events in all_events.iteritems():
            for i, event in enumerate(events):
                
                event_id = event['event_id']
                story_id = event['story_id']
                company = event['company']
                print event_id, story_id, company
#                 title = get_title(id)
                
#                 new_line = [str(id), str(event_id), str(story_id), company, title]
#                 new_line = '\t'.join(new_line) + '\n'
#                 wf.write(new_line)

if __name__ == "__main__":
#     display(analyst_ratings_event_distinction_fname, '../io/test_v2/analyst_ratings_event_distinction.txt')
    display('../io/test_v2/stock_gain_event_distinction.pkl', '../io/test_v2/stock_gain_event_distinction.txt')
