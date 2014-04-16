#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
Creation: 2014-2-25
Revision: 2014-2-25
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

import jellyfish
from timer import Timer
from util import (get_db_parser,
                  get_mysql,
                  get_update_sqlstr,
                  get_earliest_datetime,
                  get_latest_datetime,
                  get_weekly_interval,
                  transfer_str_date,
                  update_weekly_interval,
                  get_largest_event_id)
import numpy as np
import pdb

def main():
#     event_id = 0

    weeks = 0
    update_keys = ['event_id', 'story_id']
    date_field = 'media_date'
    threshold = 0.96
    mysql = get_mysql()
    event_id = get_largest_event_id(mysql) + 1
    print 'The beginning of the event_id: ', event_id
    parser = get_db_parser()
    news_title_tname = parser.get('db-in-production', 'news_title_tname')
    print news_title_tname

    earliest_datetime_in_db = get_earliest_datetime(mysql, news_title_tname, 'media_date')
    latest_datetime_in_db = get_latest_datetime(mysql, news_title_tname, 'media_date')
    with Timer() as t:
#         first, last = time_interval = get_weekly_interval(earliest_datetime_in_db)
        first, last = time_interval = ('2014-1-23', '2014-1-27')
#         first, last = time_interval = ('2014-1-6', '2014-1-13')

        while transfer_str_date(first) < latest_datetime_in_db:
            titles, idx = get_titles_and_idx(mysql, time_interval, date_field, news_title_tname)

            # 至多2000条作为一个聚类对象
            for (titles_in_a_block, idx_in_a_block) in splitting(titles, idx, block_size=2000):
                clustered, event_id = aggregating(titles_in_a_block, idx_in_a_block, threshold, event_id)

                # 注意这里的_event_id不能和event_id混淆
                for i, (id, _event_id, story_id) in enumerate(clustered.values()):
                    # 每处理100条commit一次,以后就可以采用这样的方式来处理
                    if i and not (i % 100):
                        print i
                        mysql.commit()
                    update_values = (_event_id, story_id)
                    upd_sqlstr = get_update_sqlstr(news_title_tname, update_keys, update_values, id)
                    mysql.execute(upd_sqlstr)
                else:
                    # 处理1000条之余的executed SQL queries
                    mysql.commit()

            # 测试
    #         print weeks
    #         print event_id
    #         print first, last
    #         print "# records %s" % len(titles)
    #         raw_input()

            first, last = time_interval = update_weekly_interval(time_interval)
            weeks += 1

            if not (weeks % 10):
                print "# weeks: ", weeks
            #break
    print "Timer consumed:", t.interval
    mysql.close()

#===============================================================================
# 切割层
# 当一周的新闻太多，比如：
# BETWEEN '2009-5-25' AND '2009-6-1': 68494
# BETWEEN '2014-1-6' AND '2014-1-13': 8236
# 首先将这一周的新闻切割成2000条的多个blocks,在每个block里面执行接下来的aggregating
#===============================================================================

def splitting(titles, idx, block_size=2000):
    total_size = len(titles)

    for i in xrange(0, total_size, block_size):
        yield titles[i: i + block_size], idx[i: i + block_size]

#===============================================================================
# 获取time_interval内的新闻标题及对应的id（这里用1个月作为时间间隔）
#===============================================================================

def get_titles_and_idx(mysql, time_interval, date_field, tbl_name):
    '''
    1. time_interval is like ('2003-12-01', '2004-01-01')
    2. create sql query based on the time_interval
    '''
    where_clause = "WHERE %s BETWEEN '%s' AND '%s' and event_id is null" % (date_field, time_interval[0], time_interval[1])
    order_clause = "ORDER BY %s ASC" % date_field
    select_clause = "select id, title from %s" % tbl_name

    find_sqlstr = " ".join([select_clause, where_clause, order_clause])

    titles = []
    idx = []
    for (id, title) in mysql.find(find_sqlstr):
        titles.append(title)
        idx.append(id)
    titles = np.asarray(titles, order='c')
    idx = np.asarray(idx, order='c')
    return titles, idx

#===============================================================================
# 根据阈值对新闻标题进行聚类
#===============================================================================

def aggregating(titles, idx, threshold, event_id):
    clustered = {}
    story_id = 0
    m = titles.shape[0]
    assert idx.shape[0] == m

    for i in xrange(0, m - 1):
        id_i = idx[i]

        # 如果已经被聚类,则不再被考虑
        if id_i in clustered:
            continue

        # 若为True,则clustered被更新
        flag = False
        for j in xrange(i + 1, m):
            dist = jellyfish.jaro_winkler(titles[i], titles[j])
            if dist > threshold:
                id_j = idx[j]
                if id_i not in clustered:
                    clustered[id_i] = (id_i, event_id, story_id)
                    story_id += 1
                if id_j not in clustered:
                    clustered[id_j] = (id_j, event_id, story_id)
                    story_id += 1
                flag = True
        else:
            story_id = 0

            # clustered被更新时，event_id才会被更新
            if flag:
                event_id += 1

    idx_in_clustered = set(clustered.keys())
    idx = set(idx)

    # left_idx表示独自为一个类别的新闻
    left_idx = idx - idx_in_clustered
    for each in left_idx:
        clustered[each] = (each, event_id, story_id)
        event_id += 1

    return clustered, event_id

if __name__ == "__main__":
    main()

    #===============================================================================
    # 测试
    #===============================================================================

#     titles = ['投资体制改革方案已提交国务院审批',
#               '中国第一家民营银行民生银行近期将在港上市',
#               '中国第一家民营银行民生银行近期将在港上市',
#               '投资体制改革方案已提交国务院审批',
#               ]
#     idx = [1,2,3,4]
#     event_id =0
#     threshold=0.96
#     titles = np.asarray(titles, order='c')
#     idx = np.asarray(idx, order='c')
#     clustered, event_id=aggregating(titles, idx, threshold, event_id)
#     print clustered, event_id
#     pdb.set_trace()
