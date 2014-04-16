#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: .py
Description: this program
Creation: 2014-3-15
Revision: 2014-3-15
"""

import os
import re
from pprint import pprint
from nltk import str2tuple

CURRENT_DIR = os.path.dirname(__file__)
#shougou_whitelist_word = "收购/VV"
shougou_whitelist_word = "收购"
shougou_blacklist_in_pos = set(['资产/NN', '物业/NN', '填埋场/NN'])
shougou_blacklist_in_seg = set(['终止','被否','中止','筹划','无','收购案'])

def get_fpath_based_on_flag(flag, event_type):
    fname = "%s_" % event_type + flag + '.txt'
    return os.path.join(CURRENT_DIR, '../io/test_v3/', fname)

def get_title_seg_splitted(title_pos_splitted):
    return [str2tuple(each)[0] for each in title_pos_splitted]

def get_only_pos_splitted(title_pos_splitted):
    return [str2tuple(each)[1] for each in title_pos_splitted]

def contains_blacklist_in_pos_after_shougou(blacklist_in_pos, shougou_whitelist_word,
                                            title_pos_splitted, title_seg_splitted):
    #===============================================================================
    # 对title_pos的过滤处理
    # 若黑名单的一些词出现在"收购"之后，则不是我们期望的收购事件
    #===============================================================================
    
    flag = False
    
    shougou_idx = title_seg_splitted.index(shougou_whitelist_word)
    for blackword in blacklist_in_pos:
        if blackword in title_pos_splitted:
            blackword_idx = title_pos_splitted.index(blackword)
            if shougou_idx < blackword_idx:
                flag = True
                break
    return flag, shougou_idx

def contains_blacklist_in_seg(title, shougou_blacklist_in_seg, shougou_whitelist_word):
    #===============================================================================
    # 对title_seg的过滤处理
    # 若黑名单中的词和“收购”在同一分句中出现，则不是收购事件
    #    1. 已经有了shougou_idx，也就是"收购"在分词后列表中的index
    #    2. 只以“：”和“ ”（中文的冒号和中文空格）作为句子的分隔符，对title进行处理
    #    3. 检查“收购”所在的分句是否含有黑名单的words
    #===============================================================================
    flag = False
    
    delimiters = '：| '
    for clause in re.split(delimiters, title):
        if shougou_whitelist_word in clause:
            for each in shougou_blacklist_in_seg:
                if each in clause:
                    flag = True
                    break
    
    return flag

def is_on_topic(shougou_whitelist_word, shougou_blacklist_in_pos, shougou_blacklist_in_seg,
                title, title_pos_splitted, title_seg_splitted):
    on_topic = True
    flag, shougou_idx = contains_blacklist_in_pos_after_shougou(shougou_blacklist_in_pos, shougou_whitelist_word,
                                                                title_pos_splitted, title_seg_splitted)
    if flag:
        on_topic = False
    else:
        on_topic = not contains_blacklist_in_seg(title, shougou_blacklist_in_seg, shougou_whitelist_word)
    return on_topic

def dig_into_shougou_else(fname):
    with open(fname) as f:
        for line in f:
            id, title_pos = line.strip().split('\t')
            if "并购" not in title_pos and "收购案" not in title_pos:
                print line

if __name__ == "__main__":
    raw_fname = '../io/test_v3/acqu_shougou.txt'
    
    flag1 = 'shougou_on'
    flag2 = 'shougou_off'
    flag3 = 'shougou_else'
    fpath1, fpath2, fpath3 = (get_fpath_based_on_flag(flag) for flag in (flag1, flag2, flag3))
    
    with open(raw_fname) as f:
        with open(fpath1, 'w') as f1:
            with open(fpath2, 'w') as f2:
                with open(fpath3, 'w') as f3:
                    for line in f:
                        #line = "1120999\t首旅酒店终止重组 改道收购雅客怡家\t首旅酒店/NN 终止/VV 重组/NN ，/PU 改道/NN 收购/VV 雅客怡/NR 家/NN 。/PU\n"
                        #line = "33911\t新时达终止收购湖北三环\t新时达/NR 终止/VV 收购/VV 湖/NN 北三环/NR 。/PU"
                        id, title, title_pos = line.strip().split('\t')
                        title_pos_splitted = title_pos.split()
                        title_seg_splitted = get_title_seg_splitted(title_pos_splitted)
                        if shougou_whitelist_word in title_seg_splitted:
                            if is_on_topic(shougou_whitelist_word, shougou_blacklist_in_pos, shougou_blacklist_in_seg,
                                           title, title_pos_splitted, title_seg_splitted):
                                f1.write(line)
                            else:
                                f2.write(line)
                        else:
                            f3.write(line)
                        #break
