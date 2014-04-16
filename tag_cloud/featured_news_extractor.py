#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: tag_cloud.tag_creator.py
Creation: 2013-12-31
Revision: 2013-12-31
"""

import codecs
import pdb
from collections import defaultdict
from file_system import (get_entity_extractor_fpath,
                         get_counters_fpaths,
                         get_top10_news_fpaths)

#===============================================================================
# 主函数
#===============================================================================

def extract_featured_news(current_dir, concerned_date):
    entity_extractor_fpath = get_entity_extractor_fpath(current_dir, concerned_date)

    fpaths = [entity_extractor_fpath]
    company_to_news_id, tag_to_news_id = get_mapping(fpaths)
    #pdb.set_trace()

    companies_fpath, tags_fpath = get_counters_fpaths(current_dir, concerned_date)
    print companies_fpath, tags_fpath
    top10_company_news_fpath, top10_tag_news_fpath = get_top10_news_fpaths(current_dir, concerned_date)

    get_news_id_from_company(top10_company_news_fpath, companies_fpath, company_to_news_id)
    get_news_id_from_tag(top10_tag_news_fpath, tags_fpath, tag_to_news_id)

#===============================================================================
# 根据原始数据生成两个字典：
#     1. 公司名映射到新闻id列表
#     2. 行业名称映射到新闻id列表
#===============================================================================

def get_mapping(fnames):
    company_to_news_id = defaultdict(lambda: [])
    tag_to_news_id = defaultdict(lambda: [])

    for fname in fnames:
        with open(fname) as f:
            for i, line in enumerate(f):
                if i == 0 and line[:3] == codecs.BOM_UTF8:
                    line = line[3:]

                splitted = line.strip("\n").split("|")

                # 从每一条记录提取所有字段
                news_id = splitted[0]
                date = splitted[1]
                companies = splitted[2]
                companies = list(set(each.split(":")[0] for each in companies.split(";")))
                tags = splitted[3]
                tags = list(set(each.split(":")[0] for each in tags.split(";")))

                for each in companies:
                    if each:
                        #print each
                        company_to_news_id[each].append(news_id)

                for each in tags:
                    if each:
                        #print each
                        tag_to_news_id[each].append(news_id)

    return company_to_news_id, tag_to_news_id

#===============================================================================
# 根据文件中的公司名取出相应的新闻id列表
#===============================================================================

def get_news_id_from_company(wfname, fname, company_to_news_id):
    with open(wfname, "w") as wf:
        companies_with_counters = []
        with open(fname) as f:
            for i, line in enumerate(f):
                name = line.split("::")[0]
                count = line.split("::")[1]
                count = int(count)

                companies_with_counters.append([name, count])

        print "Sorting is done!!!"
        sorted_companies_with_counters = sorted(companies_with_counters, key=lambda k: k[1], reverse=True)
        for i, each in enumerate(sorted_companies_with_counters):
            if i > 9:
                break
            #name = each[0].decode('gbk').encode('utf-8')
            name = each[0]
            #print each[0], each[1]
            news_id_list = company_to_news_id[name]
            #print news_id_list
            wf.write(",".join(news_id_list) + "\n")

#===============================================================================
# 根据文件中的行业名称取出相应的新闻id列表
#===============================================================================

def get_news_id_from_tag(wfname, fname, tag_to_news_id):
    with open(wfname, "w") as wf:
        tags_with_counters = []
        with open(fname) as f:
            for i, line in enumerate(f):
                name = line.split("::")[0]
                count = line.split("::")[1]
                count = int(count)
                tags_with_counters.append([name, count])

        for i, each in enumerate(sorted(tags_with_counters, key=lambda k: k[1], reverse=True)):
            if i > 9:
                break

            name = each[0]
            #print name
            news_id_list = tag_to_news_id[name]
            #print news_id_list
            wf.write(",".join(news_id_list) + "\n")
