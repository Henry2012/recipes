#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: arsenal.nlp.similarity.levenshtein_by_jellyfish.py
Description: this program does approximate and phonetic matching of strings
Creation: 2013-10-18
Revision: 2013-10-18
"""

#===============================================================================
# easy_install jellyfish
# https://pypi.python.org/pypi/jellyfish/0.1.2

# 常用的方法：
# - 编辑距离
# - 海明距离
# 'damerau_levenshtein_distance',
# 'hamming_distance', 
# 'jaro_distance', 
# 'jaro_winkler', 
# 'levenshtein_distance', 
# 'match_rating_codex', 
# 'match_rating_comparison', 
# 'metaphone', 
# 'nysiis', 
# 'porter_stem', 
# 'soundex'
# 详见：All-in-one (Evernote) 距离相关的知识点
#===============================================================================

import jellyfish

# print dir(jellyfish)

if __name__ == "__main__":
#     print jellyfish.levenshtein_distance('jellyfish', 'smellyfish')
#     
#     print jellyfish.jaro_distance('jellyfish', 'smellyfish')
#     
#     print jellyfish.damerau_levenshtein_distance('jellyfish', 'smellyfish')
    
    #===============================================================================
    # unicode和str是一样的效果
    #===============================================================================
#     print jellyfish.jaro_winkler(u'创业板暴跌4.37% 现巨阴断头铡', u'收评：创业板暴跌4.37% 现巨阴断头铡')
#     print jellyfish.jaro_winkler('创业板暴跌4.37% 现巨阴断头铡', '收评：创业板暴跌4.37% 现巨阴断头铡')
    
    # 不同部分出现在Title前面，对相似度影响更大
#     print jellyfish.jaro_winkler('创业板暴跌4.37% 现巨阴断头铡', '创业板暴跌4.37% 现巨阴断头铡 收评：')
    
    # 若出现更多不同部分
#     print jellyfish.jaro_winkler('创业板暴跌逾5%失1500点 个股跌停潮', '创业板暴跌逾5%失1500点 个股跌停潮逾50股跌停')
    
#     print jellyfish.jaro_winkler('地产股早盘涨跌互现 华业地产涨近6%', '地产股涨跌互现 中体产业涨4.42%')
    
#     券商股盘中上扬 兴业证券涨1.60%
#     券商股盘中震荡上扬 兴业证券涨5.5%
# 白云机场：春运刺激起降增加
# 白云机场：春运刺激起降增加 商业租赁持续较快增长
# 江海股份：薄膜电容器即将正式走向市场
# 江海股份：薄膜电容器即将正式走向市场
# 东阿阿胶：阿胶零售价上调利于终端销量提升
# 东阿阿胶：阿胶块零售价上调有利于终端销量提升
    
    # use checksums
    # 即使只是标点的差异，print的结果差别也很大。
#     import hashlib
#     print hashlib.md5("创业板暴跌逾5%失1500点 个股跌停潮").hexdigest()
#     print hashlib.md5("创业板暴跌4.37% 现巨阴断头铡。").hexdigest()
#     print hashlib.md5("创业板暴跌逾5%失1500点 个股跌停潮逾50股跌停").hexdigest()
    
    print jellyfish.levenshtein_distance('rockwell automation', 'engineeringtalk.com')
    print jellyfish.levenshtein_distance('rockwell automation', 'softswitch.com')
    print jellyfish.levenshtein_distance('rockwell automation', 'rockwellautomation.com')
