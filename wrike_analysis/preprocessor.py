#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: news_stat.preprocessor.py
Description: this program
Creation: 2013-12-6
Revision: 2013-12-6
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

import json
from collections import defaultdict

domains = defaultdict(lambda: 0)
LIMIT = 3

with open("../io/preprocessed_text_v2.txt", 'w') as wf:
    with open("../io/part-00000") as f:
        for line in f:
            
            record = json.loads(line.strip())
            print record.keys()
            
            # 有时这部分的字段和title相同，有时会更短
            # 可是鉴于有些record只有这部分展现网页内容
            print record['text']
            
            # 这部分只是content_text的一部分
            #print record.get('abstract_text', '')
            
            domain = record.get('domain', '')
            url = record.get('url', '')
            name = record.get('name', '')
            title = record.get('title', '')
            text = record.get('text', '')
            content_text = record.get('content_text', '')
            
            # 计数，每个domain只提取出3个
            domains[domain] += 1
            if domains[domain] > LIMIT:
                continue
            else:
                processed_line = "\t".join([domain, name, url, title, text, content_text]) + "\n"
                wf.write(processed_line)
            #raw_input()
