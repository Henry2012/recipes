#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: .py
Description: this program
Creation: 2014-2-12
Revision: 2014-2-12
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

#===============================================================================
# 从Stanford NLP处理后的dependency中提取规则
#===============================================================================

import re

def get_rules(sentences_fnames, rules_fname):
    rules = set()
    for sentences_fname in sentences_fnames:
        with open(sentences_fname) as f:
            for line in f:
                tagged_sent = line.strip()
                rule = get_one_rule(tagged_sent)
                if rule:
                    rules.add(rule)
            with open(rules_fname, 'w') as wf:
                for rule in rules:
                    wf.write(rule + '\n')
        
    return rules

def get_one_rule(tagged_sent):
    # Retrieve only taggers
    taggers = get_taggers(tagged_sent)
    taggers_in_str = " ".join(taggers)
    #print taggers_in_str
    
    if exists_stknm_and_keywd(taggers_in_str):
        flag = is_stknm_ahead(taggers_in_str)
        
        # Match sentences with taggers "/STKNM" & "KEYWD"
        regex_pattern = get_matching_pattern(flag)
        #print regex_pattern
        
        # Return matching rule
        matching_output = re.search(regex_pattern, taggers_in_str)
        if matching_output:
            # group matching_output
#             print "Matching"
#             print matching_output.group()
#             print matching_output.group(1)
#             print matching_output.group(3)
            
            first_group = matching_output.group(1)
            second_group = matching_output.group(2)
            third_group = matching_output.group(3)
            
            if '/PU' in second_group:
                group_output = " ".join([first_group,
                                         '/PU',
                                         third_group])
            else:
                group_output = " ".join([first_group,
                                         third_group])
            return group_output

def exists_stknm_and_keywd(taggers_in_str):
    return ('STKNM' in taggers_in_str and
            'KEYWD' in taggers_in_str)
        
def is_stknm_ahead(taggers_in_str):
    return (taggers_in_str.index('STKNM') <
            taggers_in_str.index('KEYWD'))

def get_taggers(tagged_sent):
    taggers = []
    for each in tagged_sent.strip().split():
        slash_idx = each.index('/')
        word, tagger = each[:slash_idx], each[slash_idx:]
        taggers.append(tagger)
    return taggers

def get_matching_pattern(is_stknm_ahead):
    if is_stknm_ahead:
        #pattern = r'(/[A-Z]+/STKNM).*(/[A-Z]+/KEYWD)'
        pattern = r'(/[^/]+/STKNM)(.*)(/[^/]+/KEYWD)'
    else:
        pattern = r'(/[^/]+/KEYWD)(.*)(/[^/]+/STKNM)'
    return pattern

if __name__ == "__main__":
#     tagged_sent = "午后/NT 玻璃/NN 概念股/NN 飙涨/VV/KEYWD 耀皮玻璃/VV/STKNM 涨停/VV/KEYWD 。/PU"
#     print get_one_rule(tagged_sent)

    (sentences_fname,
     rules_fname) = (['../../io/titles_contain_colon_with_one_quote_without_zhengquan_after_processed_without_hyphen_v2_seg.txt_pos_processed_v2.txt',
                      '../../io/titles_contain_colon_with_one_quote_without_zhengquan_before_processed_without_hyphen_v2_seg.txt_pos_processed_v2.txt'],
                     '../../io/rules_acquisition.txt')
    get_rules(sentences_fname, rules_fname)