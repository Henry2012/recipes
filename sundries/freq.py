#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: sundries.freq.py
Description: this program gives the freq.
Creation: 2014-1-12
Revision: 2014-1-12
"""

from collections import Counter

def get_freq(fname):
    cnt = Counter()
    with open(fname) as f:
        for line in f:
            cnt[line.strip()] += 1
    return cnt

def get_joint_freq(fnames):
    cnt = Counter()
    
    max_fname, min_fname = fnames
    with open(max_fname) as max_f:
        max_f = max_f.readlines()
        with open(min_fname) as min_f:
            for i, line in enumerate(min_f):
                min_ = line.strip()
                max_ = max_f[i].strip()
                cnt[(max_, min_)] += 1
    return cnt

if __name__ == "__main__":
    
    max_fname = "../io/max_markets_of_btc.txt"
    min_fname = "../io/min_markets_of_btc.txt"
    fnames = [max_fname, min_fname]
    #===============================================================================
    # Counter({'huobi': 203, 'btc100': 157, 'chbtc': 88, 'btcchina': 82, 'okcoin': 5})
    # Counter({'btc100': 209, 'okcoin': 165, 'btcchina': 118, 'chbtc': 31, 'huobi': 12})
    # 我想进一步调查一下：
    #    Max * Min (5*5) 一共25种情形，哪一种情形出现得最多。
    #===============================================================================
    for fname in fnames:
        freq = get_freq(fname)
        print freq
        
    joint_freq = get_joint_freq(fnames)
    print joint_freq