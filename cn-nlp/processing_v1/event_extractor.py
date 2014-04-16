#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: .py
Description: this program
Creation: 2014-1-27
Revision: 2014-1-27
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

#===============================================================================
# 利用关键字进行事件分类
# 接收的参数：
#     新闻的标题和所有股票名简称
# 返回值：
#     事件类型和提及的公司名列表
#===============================================================================

import re
from util import get_related_companies

type1 = ('acquisitions-mergers', 'acquisition', 'completed', 'acquisition-completed-acquiree')
type2 = ('acquisitions-mergers', 'acquisition', 'plan', 'acquisition-acquiree')
type3 = ('earnings', 'earnings', 'above-expectations', 'earnings-above-expectations')
type4 = ('earnings', 'earnings-estimate', 'upgrade', 'earnings-estimate-upgrade')
type5 = ('stock-prices', 'stock', 'gain', 'stock-gain')
type6 = ('insider-trading', 'shareholder-buy', '', 'shareholder-buy')
type7 = ('products-services', 'product-release', '', 'product-release')

def process_acquisition(title, stock_quotes):
    output = None
    if "收购" in title:
        related_companies = get_related_companies(title, stock_quotes)
#         post_processed_companies = []
#         for each in related_companies:
#             if "证券" not in each:
#                 post_processed_companies.append(each)

        if '拟收购' in title:
            output = type2, post_processed_companies
        else:
            output = type1, post_processed_companies
    return output

def process_earnings(title, stock_quotes):
    output = None

    if (('净利润' in title or
        '收入' in title or
        '利润' in title or
        '营收' in title or
        '业绩' in title) and
        ('超预期' in title or
         '超于预期' in title or
         '向上修正' in title)):
        related_companies = get_related_companies(title, stock_quotes)
        output = type3, related_companies
    elif (('净利润' in title or
        '收入' in title or
        '利润' in title or
        '营收' in title or
        '业绩' in title) and
        ('上调' in title or
         '提高' in title)):
        related_companies = get_related_companies(title, stock_quotes)
        output = type4, related_companies

    return output

def process_zhenchi(title, stock_quotes):
    output = None

    pattern = '增持.*股'

    if re.search(pattern, title):
        related_companies = get_related_companies(title, stock_quotes)
        output = type6, related_companies

    return output

def process_gaining_stock(title, stock_quotes):
    output = None
    
    if ("大涨" in title or
        "领涨" in title or
        "涨停" in title):
        related_companies = get_related_companies(title, stock_quotes)
        if related_companies:
            output = type5, related_companies

    return output

def process_product_release(title, stock_quotes):
    output = None

    if ("交付" in title or
        "发布" in title or
        "改版" in title or
        "升级" in title):
        related_companies = get_related_companies(title, stock_quotes)
        if related_companies:
            output = type7, related_companies

    return output
