#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: tag_cloud.processor.py
Creation: 2014-1-10
Revision: 2014-1-10
"""

import datetime
import os
import sys

from entity_extractor import extract_entity
from preprocessor import sort_entity_extractor
from counter_processor import process_counter
from featured_news_extractor import extract_featured_news
from insert import insert_into_mysql
from title_collector import collect_titles
from email_sender import send_status_from_tag_cloud

CURRENT_DIR = os.path.dirname(__file__)
concerned_date = sys.argv[1]
#concerned_dtime = datetime.datetime.now()
#concerned_date = concerned_dtime.strftime('%Y-%-m-%-d')

extract_entity(CURRENT_DIR, concerned_date)
sort_entity_extractor(CURRENT_DIR, concerned_date)
process_counter(CURRENT_DIR, concerned_date)
extract_featured_news(CURRENT_DIR, concerned_date)
collect_titles(CURRENT_DIR, concerned_date)
send_status_from_tag_cloud("Data-involved Processing is done!!!")
insert_into_mysql(CURRENT_DIR, concerned_date)
send_status_from_tag_cloud("All is done!!!")
