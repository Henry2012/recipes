#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: .py
Description: this program
Creation: 2014-2-13
Revision: 2014-2-13
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

import os
import pdb
import sys
basepath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(basepath, "..")))

from util import (STOCK_GAIN_KW,
                  PRODUCT_RELEASE_KW,
                  ACQUISITION_KW,
                  get_stock_quotes)
from file_names import (stock_quote_fname,
                        colon_with_one_quote_without_zhengquan_before_colon_without_hyphen_fname,
                        colon_with_one_quote_without_zhengquan_after_colon_without_hyphen_fname,
                        colon_with_one_quote_without_zhengquan_after_colon_revised_without_hyphen_fname,
                        colon_with_one_quote_without_zhengquan_before_colon_revised_without_hyphen_fname,
                        colon_with_more_quotes_without_hyphen_without_zhengquan_and_colon_fname,
                        stock_gain_fname,
                        non_stock_gain_fname,
                        product_release_fname,
                        non_product_release_fname,
                        acquisition_fname,
                        non_acquisition_fname)

def get_event_from_one_quote(fname,
                             event_kw,
                             event_fname,
                             non_event_fname):
    with open(fname) as f:
        with open(event_fname, 'a') as wf1:
            with open(non_event_fname, 'a') as wf2:
                count = 0
                for line in f:
                    title = line.strip().split('\t')[1]
                    
                    has_kw = False
                    for kw in event_kw:
                        if kw in title:
                            has_kw = True
                            break
                    
                    if has_kw:
                        count += 1
                        wf1.write(line)
                    else:
                        wf2.write(line)
    return count

def get_event_from_more_quotes(fname,
                                stock_quotes,
                                event_kw,
                                event_fname,
                                non_event_fname):
    count = 0
    with open(fname) as f:
        with open(event_fname, 'a') as wf1:
            with open(non_event_fname, 'a') as wf2:
                for line in f:
                    is_event = False
                    concerned_companies = set()
                    id, sent, companies = line.strip().split('\t')
                    front, behind = sent.split("：", 1)
                    clauses = behind.split(" ")

                    has_kw = False
                    for kw in event_kw:
                        if kw in sent:
                            has_kw = True
                            break
     
                    if has_kw:
                        for clause in clauses:
                            for kw in event_kw:
                                if kw in clause:
                                    for stock_quote in stock_quotes:
                                        if stock_quote in clause:
                                            concerned_companies.add(stock_quote)
                        if not concerned_companies:
                            for stock_quote in stock_quotes:
                                if stock_quote in front:
                                    concerned_companies.add(stock_quote)
                         
                        if not concerned_companies:
                            indice = []
                            for stock_quote in stock_quotes:
                                if stock_quote in clauses[0]:
                                    idx = clauses[0].index(stock_quote)
                                    indice.append((stock_quote, idx))
                            company = sorted(indice, key=lambda k: k[1])[0][0]
                            concerned_companies.add(company)
                         
                        if concerned_companies:
                            companies_in_str = '>|<'.join(concerned_companies)
                            is_event = True
                            count += 1
                            wf1.write('\t'.join([id, sent, companies_in_str]) + '\n')
                             
                    if not is_event:
                        wf2.write(line)
    return count

def get_event_via_segmented_sent(segmented_sentences_fname,
                                      event_kw,
                                      event_fname,
                                      stock_quotes):
    line_no = []
    with open(segmented_sentences_fname) as f:
        with open(event_fname, 'w') as wf:
            for i, line in enumerate(f):
                sent = line.strip().split('\t')[0]
                splited_sent = set(sent.split())
                
                has_kw = False
                for kw in event_kw:
                    if kw in splited_sent:
                        has_kw = True
                        break
                
                has_quote = True
#                 for quote in stock_quotes:
#                     if quote in splited_sent:
#                         has_quote = True
#                         break
                
                if has_kw and has_quote:
                    line_no.append(i)
                    wf.write(line)
    return line_no

# def get_stock_gain(raw_fname,
#                     stock_gain_kw,
#                     stock_gain_fname,
#                     non_stock_gain_fname,
#                     stock_quotes):
#      
#     with open(raw_fname) as f:
#         with open(stock_gain_fname, 'w') as wf:
#             with open(non_stock_gain_fname, 'w') as wf2:
#                 for line in f:
#                     is_event = False
#                     concerned_companies = set()
#                     sent, companies = line.strip().split('\t')
#                     front, behind = sent.split("：", 1)
#                     clauses = behind.split(" ")
# 
#                     has_kw = False
#                     for kw in stock_gain_kw:
#                         if kw in sent:
#                             has_kw = True
#                             break
#      
#                     if has_kw:
#                         for clause in clauses:
#                             for kw in stock_gain_kw:
#                                 if kw in clause:
#                                     for stock_quote in stock_quotes:
#                                         if stock_quote in clause:
#                                             concerned_companies.add(stock_quote)
#                         if not concerned_companies:
#                             for stock_quote in stock_quotes:
#                                 if stock_quote in front:
#                                     concerned_companies.add(stock_quote)
#                          
#                         if not concerned_companies:
#                             indice = []
#                             for stock_quote in stock_quotes:
#                                 if stock_quote in clauses[0]:
#                                     idx = clauses[0].index(stock_quote)
#                                     indice.append((stock_quote, idx))
#                             company = sorted(indice, key=lambda k: k[1])[0][0]
#                             concerned_companies.add(company)
#                          
#                         if concerned_companies:
#                             companies_in_str = '>|<'.join(concerned_companies)
#                             is_event = True
#                             wf.write('\t'.join([sent, companies, companies_in_str]) + '\n')
#                              
#                     if not is_event:
#                         wf2.write(line)

if __name__ == "__main__":
    #===============================================================================
    # Get all stock quotes
    #===============================================================================

    STOCK_QUOTES = get_stock_quotes(stock_quote_fname)
    
    one_quote_fnames = (colon_with_one_quote_without_zhengquan_before_colon_without_hyphen_fname,
                        colon_with_one_quote_without_zhengquan_after_colon_without_hyphen_fname)
    
#     one_quote_revised_fnames = (colon_with_one_quote_without_zhengquan_after_colon_revised_without_hyphen_fname,
#                                 colon_with_one_quote_without_zhengquan_before_colon_revised_without_hyphen_fname)
    print "# of keywords: ", len(PRODUCT_RELEASE_KW)
    count = 0
    for fname in one_quote_fnames:
        count += get_event_from_one_quote(fname,
                                      PRODUCT_RELEASE_KW,
                                      product_release_fname,
                                      non_product_release_fname)

    count += get_event_from_more_quotes(colon_with_more_quotes_without_hyphen_without_zhengquan_and_colon_fname,
                                    STOCK_QUOTES,
                                    PRODUCT_RELEASE_KW,
                                    product_release_fname,
                                    non_product_release_fname)
    print count

#     (segmented_sentences_fname,
#      segmented_sentences_fname_2,
#      raw_fname,
#      stock_gain_fname_tier_1,
#      stock_gain_fname_tier_2,
#      non_stock_gain_fname_tier_2,
#      stock_quote_fname) = get_absolute_paths(('titles_contain_colon_with_one_quote_without_zhengquan_after_colon_processed_without_hyphen_v2_seg_modified.txt',
#                                              'titles_contain_colon_with_one_quote_without_zhengquan_before_colon_processed_without_hyphen_v2_seg_modified.txt',
#                                              'titles_contain_colon_with_more_quotes_without_hyphen_without_zhengquan_and_colon.txt',
#                                              'stock_gain_v4.txt',
#                                              'stock_gain_tier_2_v2.txt',
#                                              'non_stock_gain_tier_2_v2.txt',
#                                             'stock_quotes.txt'),
#                                             dir_name='../io/')
#  
#     STOCK_QUOTES = get_stock_quotes(stock_quote_fname)
#     line_no = get_stock_gain_via_segmented_sent(segmented_sentences_fname,
#                                       STOCK_GAIN_KW,
#                                       stock_gain_fname_tier_1,
#                                       STOCK_QUOTES)
# 
#     id_no = []
#     with open(colon_with_one_quote_without_zhengquan_after_colon_without_hyphen_fname) as f:
#         f = f.readlines()
#         for each in line_no:
#             id_no.append(f[each].strip().split("\t")[0])
#     
#     pdb.set_trace()
#     with open('../io/record_id.txt', 'w') as wf:
#         for id in id_no:
#             wf.write(id + '\n')
#     
#     new_id_no = []
#     with open(stock_gain_fname) as f:
#         for line in f:
#             new_id_no.append(line.strip().split('\t')[0])
#     
#     pdb.set_trace()
#     
#     with open('../io/new_identified_id.txt','w') as wf:
#         with open(stock_gain_fname) as f:
#             f = f.readlines()
#             for id in set(new_id_no) - set(id_no):
#                 
#                 wf.write(id + '\n')
            
        

#     get_stock_gain(raw_fname,
#                     STOCK_GAIN_KW,
#                     stock_gain_fname_tier_2,
#                     non_stock_gain_fname_tier_2,
#                     STOCK_QUOTES)