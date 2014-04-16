#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: sundries.preprocess_titles.py
Description: this program
Creation: 2014-2-11
Revision: 2014-2-11
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

import codecs
import nltk
import os
import pdb
import re
import sys
basepath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(basepath, "..")))

from util import (get_related_companies,
                  get_stock_quotes,
                  STOCK_GAIN_KW,
                  PRODUCT_RELEASE_KW,
                  get_fnames)

def process_titles_concerning_signs(raw_fname, colon_fname, blank_without_colon_fname, all_else_fname):
    with open(raw_fname) as f:
        with open(colon_fname, 'w') as colon_wf:
            with open(blank_without_colon_fname, 'w') as blank_without_colon_wf:
                with open(all_else_fname, 'w') as all_else_wf:
                    count = 0
                    for line in f:
                        if line == '\n':
                            continue
                        
                        count += 1
                        
                        if not (count % 100):
                            print "[ INFO ] # of lines processed: %s" % count

                        # get detailed info
                        detailed_info = get_details_info_from_raw_record(line)
                        title = detailed_info['title']
                        id = detailed_info['id']
                        
                        # initiate
                        new_line = "\t".join([id, title]) + '\n'
                        
                        if (":" in title or
                            "：" in title):
                            title = title.replace(":", '：')
                            new_line = "\t".join([id, title]) + '\n'
#                             print 'colon'
#                             print title
#                             print new_line
                            colon_wf.write(new_line)
                        elif " " in title:
#                             print 'blank'
#                             print [title]
#                             print new_line
                            blank_without_colon_wf.write(new_line)
                        else:
#                             print 'all else'
#                             print title
#                             print new_line
                            all_else_wf.write(new_line)

def process_titles_concerning_quotes(stock_quotes, raw_fname,
                              zero_quote_fname, one_quote_fname, more_quotes_fname):
    with open(raw_fname) as f:
        with open(zero_quote_fname, 'w') as wf0:
            with open(one_quote_fname, 'w') as wf1:
                with open(more_quotes_fname, 'w') as wf2:
                    for i, line in enumerate(f):
                        if not (i % 100):
                            print i
                        id, title = line.strip().split('\t')
                        related_companies = get_related_companies(title, stock_quotes)
                        
                        if not related_companies:
                            wf0.write(line)
                        elif len(related_companies) == 1:
                            related_companies = list(related_companies)[0]
                            new_line = "\t".join([id, title, related_companies]) + '\n'
                            wf1.write(new_line)
                        else:
                            related_companies = ">|<".join(related_companies)
                            new_line = "\t".join([id, title, related_companies]) + '\n'
                            wf2.write(new_line)

def process_titles_concerning_zhengquan(one_quote_fname,
                                        one_quote_fname_with_zhengquan,
                                        one_quote_fname_without_zhengquan):
    with open(one_quote_fname) as f:
        with open(one_quote_fname_with_zhengquan, 'w') as wf1:
            with open(one_quote_fname_without_zhengquan, 'w') as wf2:
                for line in f:
                    id, title, company = line.strip().split("\t")
                    if "证券" in company:
                        wf1.write(line)
                    else:
                        wf2.write(line)

def process_titles_concerning_quote_and_colon_position(titles_with_quotes_fname,
                                                       before_colon_fname,
                                                       after_colon_fname):
    #===============================================================================
    # 至少有一个公司出现在冒号前的记录保存在 before_colon_fname
    #===============================================================================
    with open(titles_with_quotes_fname) as f:
        with open(before_colon_fname, 'w') as wf1:
            with open(after_colon_fname, 'w') as wf2:
                for line in f:
                    if not line:
                        continue
                    id, title, companies = line.strip().split('\t')
                    companies = companies.split('>|<')
                    for company in companies:
                        if company in title.split("：")[0]:
                            wf1.write(line)
                            break
                    else:
                        wf2.write(line)

#===============================================================================
# 这个版本的函数处理的文件只有title这一列
#===============================================================================
# def process_titles_concerning_quote_and_colon_position(titles_fname,
#                                                        before_colon_fname,
#                                                        after_colon_fname,
#                                                        stock_quotes):
#     with open(titles_fname) as f:
#         with open(before_colon_fname, 'w') as wf1:
#             with open(after_colon_fname, 'w') as wf2:
#                 for line in f:
#                     if not line:
#                         continue
#                     title = line.strip()
#                     companies = get_related_companies(title, stock_quotes)
#                     for company in companies:
#                         if company in title.split("：")[0]:
#                             wf1.write(line)
#                             break
#                     else:
#                         wf2.write(line)

#===============================================================================
# 利用强关键字进行topic classification不需要接下来对新闻标题的修改
#===============================================================================

def revise_titles_with_quote_name_after_colon(after_colon_fname,
                                              after_colon_fname_processed):
    with open(after_colon_fname) as f:
        with open(after_colon_fname_processed, 'w') as wf:
            for line in f:
                splitted = line.strip().split("\t")
                title = splitted[1]
                
                # 替换全角和半角空格
                new_title = title.replace(' ', '，').replace('　', '，')
                
                if not new_title.endswith("："):
                    new_title = new_title.split("：", 1)[1] + '。'

                    # 替换书名号和引号
                    new_title = new_title.replace('《', ' ').replace("》", " ")
                    new_title = new_title.replace("‘", ' ').replace('’', ' ')
                    new_title = new_title.replace('“', ' ').replace('”', ' ')

                    splitted[1] = new_title
                    new_line = "\t".join(splitted) + '\n'
                    wf.write(new_line)

#===============================================================================
# 利用强关键字进行topic classification不需要接下来对新闻标题的修改
#===============================================================================

def revise_titles_with_quote_name_before_colon(before_colon_fname,
                                               before_colon_fname_processed):
    with open(before_colon_fname) as f:
        with open(before_colon_fname_processed, 'w') as wf:
            for line in f:
                splitted = line.strip().split("\t")
                title = splitted[1]
                
                new_title = title.replace(' ', '，').replace('：', '，').replace('　', '，') + "。"
                
                # 替换书名号和引号
                new_title = new_title.replace('《', ' ').replace("》", " ")
                new_title = new_title.replace("‘", ' ').replace('’', ' ')
                new_title = new_title.replace('“', ' ').replace('”', ' ')
                
                splitted[1] = new_title
                new_line = "\t".join(splitted) + '\n'
                wf.write(new_line)

def process_titles_concerning_hyphen(fname,
                                     new_fname_with_pattern,
                                     new_fname_without_pattern):
    with open(fname) as f:
        with open(new_fname_without_pattern, 'w') as wf1:
            with open(new_fname_with_pattern, 'w') as wf2:
                for line in f:
                    title = line.strip().split('\t')[1]
                    if not re.search(r".+-.+：", title):
                        wf1.write(line)
                    else:
                        wf2.write(line)

def process_titles_tagged(tagged_fname,
                          tagged_fname_processed,
                          stock_quote_fname,
                          keywords=STOCK_GAIN_KW):
    stock_quotes = get_stock_quotes(stock_quote_fname)
    zhang_keywords = []
    with open(tagged_fname) as f:
        with open(tagged_fname_processed, 'w') as wf:
            for line in f:
                # preprocess
                preprocessed_line = [list(nltk.str2tuple(each)) for each in line.strip().split()]
                for i, (word, tagger) in enumerate(preprocessed_line):
                    # Add stock name tagger
                    if word in stock_quotes:
                        new_tagger = tagger + '/STKNM'
                        preprocessed_line[i] = [word, new_tagger]

                    # Add keyword tagger
                    #assert len(keywords) == 4
                    for keyword in keywords:
#                         print keyword
#                         print word
#                         raw_input()
                        if keyword in word:
                            #print "existing"
                            new_tagger = tagger + '/KEYWD'
                            preprocessed_line[i] = [word, new_tagger]
                    
                    # Count all words containing “涨”
                    if "涨" in word:
                        zhang_keywords.append(word)

                new_line_in_str = " ".join("/".join(each) for each in preprocessed_line) + '\n'
                wf.write(new_line_in_str)
    return zhang_keywords

# old version
# def process_titles_with_colon(colon_fname, processed_fname, stock_quote_fname):
#     with open(colon_fname) as f:
#         with open(processed_fname, 'w') as wf:
#             for line in f:
#                 title = line.strip()
#                 processed_title = title.split("：")[1].replace(" ", '，')
#                 new_line = '\t'.join([title, processed_title+"\n"])
#                 wf.write(new_line)

def process_titles_with_blank(blank_fname, processed_fname):
    with open(blank_fname) as f:
        with open(processed_fname, 'w') as wf:
            for line in f:
                title = line.strip()
                processed_title = title.replace(' ', '，').split('：')
                if len(processed_title) > 1:
                    processed_title = processed_title[1]
                else:
                    processed_title = processed_title[0]
                new_line = '\t'.join([title, processed_title+"\n"])
                wf.write(new_line)

def process_titles_concerning_zhengquan_and_colon(fname,
                                                  new_fname_without_pattern,
                                                  new_fname_with_pattern):
    with open(fname) as f:
        with open(new_fname_without_pattern, 'w') as wf1:
            with open(new_fname_with_pattern, 'w') as wf2:
                for line in f:
                    title = line.strip().split('\t')[1]
                    if '证券：' not in title:
                        wf1.write(line)
                    else:
                        wf2.write(line)

#===============================================================================
# deprecated
# 记录的结构还没有固定
#===============================================================================

def get_details_info_from_raw_record(record):
    return dict(zip(['id', 'title', 'media_date', 'source'],
                    record.strip().split('\t')))

#===============================================================================
# 用于ratings事件的预处理：
#     1. records_with_colon_with_one_quote_without_zhengquan_before_colon_with_hyphen
#         + 提取出唯一公司名出现在第一个连字符和第一个冒号之间的记录
#     2. records_with_colon_with_more_quotes_fname_with_hyphen
#         + 提取出出现在第一个连字符和第一个冒号之间的公司名
#===============================================================================

def process_titles_concerning_one_quote_and_hyphen_position(fname,
                                                            quote_after_first_hyphen_fname,
                                                            quote_before_first_hyphen_fname):
    with open(fname) as f:
        with open(quote_after_first_hyphen_fname, 'w') as wf1:
            with open(quote_before_first_hyphen_fname, 'w') as wf2:
                for line in f:
                    id, title, company = line.strip().split('\t')
                    
                    # 判断唯一的公司名是否在第一个连字符之后，初始文件已经保证了该公司名在第一个冒号之前
                    front, behind = title.split('-', 1)
                    if (behind and
                        company in behind):
                        wf1.write(line)
                    else:
                        wf2.write(line)

def process_titles_concerning_all_quotes_and_hyphen_position(fname,
                                                              all_quotes_before_colon_fname,
                                                              not_all_quotes_before_colon_fname):
    #===============================================================================
    # 出现的所有公司名都在冒号之前才能存放在 all_quotes_before_colon_fname
    #===============================================================================
    with open(fname) as f:
        with open(all_quotes_before_colon_fname, 'w') as wf1:
            with open(not_all_quotes_before_colon_fname, 'w') as wf2:
                for line in f:
                    id, title, companies = line.strip().split('\t')
                    companies = companies.split('>|<')
                    
                    front, behind = title.split('：', 1)
                    is_all_quotes_before_colon = all(comp in front for comp in companies)
                    
                    if is_all_quotes_before_colon:
                        wf1.write(line)
                    else:
                        wf2.write(line)

#===============================================================================
# Deprecated
# 函数中对个别中文字符的处理会放在某些操作之后，而不是作为预处理
#===============================================================================

def replace_special_characters_before_seg(raw_fname,
                                          updated_fname):
    with open(raw_fname) as f:
        with open(updated_fname, 'w') as wf:
            for line in f:
                splitted_line = line.strip().split('\t')
                title = splitted_line[1]
                
                new_title = title.replace('《', ' ').replace("》", " ")
                new_title = new_title.replace("‘", ' ').replace('’', ' ')
                new_title = new_title.replace('“', ' ').replace('”', ' ')
                
                splitted_line[1] = new_title
                new_line = '\t'.join(splitted_line) + '\n'
                wf.write(new_line)

if __name__ == "__main__":
    raw_fname = "../../io/titles.txt"
    stock_quote_fname = "../../io/stock_quotes.txt"
    zhang_keyword_fname = '../../io/zhang_keywords.txt'
    product_keyword_fname = '../../io/product_keywords.txt'
    tagged_fnames = (
    '../../io/titles_contain_colon_with_one_quote_without_zhengquan_after_processed_without_hyphen_v2_seg.txt_pos.txt',
    '../../io/titles_contain_colon_with_one_quote_without_zhengquan_before_processed_without_hyphen_v2_seg.txt_pos.txt')
                    
    tagged_fnames_processed = (
    '../../io/titles_contain_colon_with_one_quote_without_zhengquan_after_processed_without_hyphen_v2_seg.txt_pos_processed_v2.txt',
    '../../io/titles_contain_colon_with_one_quote_without_zhengquan_before_processed_without_hyphen_v2_seg.txt_pos_processed_v2.txt')
    
    colon_fname = "../../io/titles_contain_colon.txt"
    new_colon_fname = "../../io/titles_contain_colon_processed.txt"
    zero_quote_fname, one_quote_fname, more_quotes_fname = ('../../io/titles_contain_colon_with_zero_quotes.txt',
                                                            '../../io/titles_contain_colon_with_one_quote.txt',
                                                            '../../io/titles_contain_colon_with_more_quotes.txt')
    (one_quote_fname_with_zhengquan,
     one_quote_fname_without_zhengquan) = ('../../io/titles_contain_colon_with_one_quote_with_zhengquan.txt',
                                           '../../io/titles_contain_colon_with_one_quote_without_zhengquan.txt')
    (before_colon_fname,
     after_colon_fname,
     before_colon_fname_processed,
     after_colon_fname_processed,
     before_colon_fname_processed_without_hyphen,
     after_colon_fname_processed_without_hyphen,
     before_colon_fname_processed_with_hyphen,
     after_colon_fname_processed_with_hyphen,) = ('../../io/titles_contain_colon_with_one_quote_without_zhengquan_before.txt',
                                                    '../../io/titles_contain_colon_with_one_quote_without_zhengquan_after.txt',
                                                    '../../io/titles_contain_colon_with_one_quote_without_zhengquan_before_processed.txt',
                                                    '../../io/titles_contain_colon_with_one_quote_without_zhengquan_after_processed.txt',
                                                    '../../io/titles_contain_colon_with_one_quote_without_zhengquan_before_processed_without_hyphen_v2.txt',
                                                    '../../io/titles_contain_colon_with_one_quote_without_zhengquan_after_processed_without_hyphen_v2.txt',
                                                    '../../io/titles_contain_colon_with_one_quote_without_zhengquan_before_processed_with_hyphen_v2.txt',
                                                    '../../io/titles_contain_colon_with_one_quote_without_zhengquan_after_processed_with_hyphen_v2.txt',)
     

    blank_fname = "../../io/titles_contain_blank.txt"
    new_blank_fname = "../../io/titles_contain_blank_processed.txt"
    none_fname = "../../io/titles_contain_none.txt"

#     get_titles_concerning_signs(raw_fname, colon_fname, blank_fname, none_fname)

#     process_titles_with_colon(colon_fname, new_colon_fname)
#     process_titles_with_blank(blank_fname, new_blank_fname)
    
#     stock_quotes = get_stock_quotes(stock_quote_fname)
#     pdb.set_trace()

#     process_titles_with_colon(colon_fname, stock_quote_fname,
#                               zero_quote_fname, one_quote_fname, more_quotes_fname)

#     process_titles_with_colon_and_one_quote(one_quote_fname,
#                                             one_quote_fname_with_zhengquan,
#                                             one_quote_fname_without_zhengquan)

#     process_titles_with_quotes_concerning_quote_and_colon_position(one_quote_fname_without_zhengquan,
#                                                               before_colon_fname,
#                                                               after_colon_fname)
    
#     process_titles_with_colon_and_one_quote_without_zhengquan_after(after_colon_fname,
#                                                                     after_colon_fname_processed)
#     
#     process_titles_with_colon_and_one_quote_without_zhengquan_before(before_colon_fname,
#                                                                      before_colon_fname_processed)

#     process_titles_concerning_hyphen(before_colon_fname_processed,
#                               before_colon_fname_processed_without_hyphen,
#                               before_colon_fname_processed_with_hyphen)
#     process_titles_concerning_hyphen(after_colon_fname_processed,
#                               after_colon_fname_processed_without_hyphen,
#                               after_colon_fname_processed_with_hyphen)

#     zhang_keywords = []
#     for (tagged_fname, tagged_fname_processed) in zip(tagged_fnames, tagged_fnames_processed):
#          
#         zhang_keywords.extend(process_titles_tagged(tagged_fname,
#                                                     tagged_fname_processed,
#                                                     stock_quote_fname,
#                                                     keywords=["收购"]))

#     with open(product_keyword_fname, 'w') as wf:
#         for each in set(zhang_keywords):
#             wf.write(each + '\n')
