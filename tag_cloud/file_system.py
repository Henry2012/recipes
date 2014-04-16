#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: tag_cloud.file_system.py
Creation: 2014-1-10
Revision: 2014-1-10
"""

import os

COUNTERS = ['io/counters/companies',
            'io/counters/tags']
TOP10_NEWS = ['io/top10_news/companies',
              'io/top10_news/tags']
ENTITY_EXTRACTOR = 'io/entity_extractor'
MERGED = 'io/merged'
NEWS_ID = 'io/news_id.txt'

def get_counters_fpaths(current_dir, concerned_date):
    fname = "%s.txt" % concerned_date

    output = []
    for each in COUNTERS:
        fpath = os.path.join(current_dir, each, fname)
        fpath = os.path.abspath(fpath)
        output.append(fpath)
    return output

def get_top10_news_fpaths(current_dir, concerned_date):
    fname = "%s.txt" % concerned_date

    output = []
    for each in TOP10_NEWS:
        fpath = os.path.join(current_dir, each, fname)
        fpath = os.path.abspath(fpath)
        output.append(fpath)
    return output

def get_top10_news_title_fpaths(current_dir, concerned_date):
    fname = "%s-titles.txt" % concerned_date

    output = []
    for each in TOP10_NEWS:
        fpath = os.path.join(current_dir, each, fname)
        fpath = os.path.abspath(fpath)
        output.append(fpath)
    return output

def get_entity_extractor_fpath(current_dir, concerned_date):
    fname = "%s.txt" % concerned_date
    fpath = os.path.join(current_dir, ENTITY_EXTRACTOR, fname)
    fpath = os.path.abspath(fpath)
    return fpath

def get_entity_extractor_sorted_fpath(current_dir, concerned_date):
    fname = "%s-sorted.txt" % concerned_date
    fpath = os.path.join(current_dir, ENTITY_EXTRACTOR, fname)
    fpath = os.path.abspath(fpath)
    return fpath

def get_merged_fpath(current_dir, concerned_date):
    fname = "%s.txt" % concerned_date
    fpath = os.path.join(current_dir, MERGED, fname)
    fpath = os.path.abspath(fpath)
    return fpath

def get_news_id_fpath(current_dir):
    fpath = os.path.join(current_dir, NEWS_ID)
    fpath = os.path.abspath(fpath)
    return fpath

if __name__ == "__main__":

    concerned_date = "2014-1-9"
    current_dir = os.path.dirname(__file__)

    print get_counters_fpaths(current_dir, concerned_date)
    print get_top10_news_fpaths(current_dir, concerned_date)
    print get_top10_news_title_fpaths(current_dir, concerned_date)
    print get_entity_extractor_fpath(current_dir, concerned_date)
    print get_entity_extractor_sorted_fpath(current_dir, concerned_date)
    merged_fpath = get_merged_fpath(current_dir, concerned_date)
    print merged_fpath
    print get_news_id_fpath(current_dir)

    #with open(merged_fpath) as f:
    #    for line in f:
    #        print line
    #        break
