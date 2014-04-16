#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: textblob.recipes.py
Description: this program offers snippets to process simplified text
Creation: 2013-11-11
Revision: 2013-11-11
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

import os
from textblob import TextBlob

fname = os.path.abspath(os.path.join(os.path.dirname(__file__),
                             "..",
                             'io/data_preparation_for_simplified_text_processing.txt'))
with open(fname) as f:
    text = f.read()
    blob = TextBlob(text)
 
#     np = blob.noun_phrases
#      
#     for each in np:
#         print each
    for each in blob.word_counts:
        print each

# print dir(TextBlob)
