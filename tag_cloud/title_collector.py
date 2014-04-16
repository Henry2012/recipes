# -*- coding: utf-8 -*-
# Author: Peng Chao
# Copyright: EverString
# Date:
# Distributed under terms of the EverString license.

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from file_system import (get_top10_news_fpaths,
                         get_top10_news_title_fpaths,
                         get_merged_fpath,
                         get_news_id_fpath)

def collect_titles(current_dir, concerned_date):
    top10_news_fpaths = get_top10_news_fpaths(current_dir, concerned_date)
    top10_news_title_fpaths = get_top10_news_title_fpaths(current_dir, concerned_date)
    merged_fpath = get_merged_fpath(current_dir, concerned_date)
    news_id_fpath = get_news_id_fpath(current_dir)

    with open(news_id_fpath) as news_id:
        first_news_id = int(news_id.read()) + 1

    with open(merged_fpath) as merged:
        merged = merged.readlines()
        for i, top10_news_fpath in enumerate(top10_news_fpaths):
            with open(top10_news_fpath) as top10_news:
                with open(top10_news_title_fpaths[i], 'w') as top10_news_title:
                    for line in top10_news:
                        ids = line.strip().split(',')
                        for id in ids:
                            line_index = int(id) - first_news_id
                            news_required = merged[line_index]

                            # strip时不指定"\n",反而能够兼容Unix和Windows两个系统下不同的换行符
                            splitted = news_required.strip().split(">|<")
                            news_title = splitted[2]
                            news_url = splitted[-1]

                            top10_news_title.write("|".join([news_title, news_url]) + "\r\n")
                        top10_news_title.write("\r\n")

if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    concerned_date = '2014-1-16'
    collect_titles(current_dir, concerned_date)
