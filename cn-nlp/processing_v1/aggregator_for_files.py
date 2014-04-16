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
from util import (get_db_parser,
                  get_mysql,
                  save_cpickle,
                  load_cpickle,
                  get_update_sqlstr)
from cluster import HierarchicalClustering
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import (fclusterdata,
                                     fcluster)
import numpy as np
import pdb

def main(output_source):
    update_keys = ['event_id_dist96', 'story_id']
    mysql = get_mysql()
    parser = get_db_parser()
    news_title_tname = parser.get('db-in-production', 'news_title_tname')
    
    data_info = load_cpickle(output_source)
    for i, (id, event_id, story_id) in enumerate(data_info.values()):
        if not (i % 100):
            print i
        update_values = (event_id, story_id)
        upd_sqlstr = get_update_sqlstr(news_title_tname, update_keys, update_values, id)
#         print upd_sqlstr
#         raw_input()
        mysql.execute(upd_sqlstr)
    mysql.commit()
    
def get_titles_and_idx(fname):
    titles = []
    idx = []
    with open(fname) as f:
        for line in f:
            splitted = line.strip().split('\t')
            if len(splitted) == 1:
                title = splitted[0]
            elif len(splitted) == 2:
                id, title = splitted
                idx.append(int(id))
            titles.append(title)
        titles = np.asarray(titles, order='c')    
        idx = np.asarray(idx, order='c')
    return titles, idx

def get_distance_matrix(X, threshold):
    clusters = []
    m = X.shape[0]
#     print m
       
    # distance matrix
    dm = np.zeros((m * (m - 1)) // 2, dtype=np.int8)
    k = 0
    for i in xrange(0, m - 1):
        for j in xrange(i + 1, m):
            dist = jellyfish.jaro_winkler(X[i], X[j])
            if dist > threshold:
                dm[k] = 1
            k = k + 1
    return dm

def aggregating(titles, idx, threshold):
    clustered = {}
    event_id = 0
    story_id = 0
    m = titles.shape[0]
    assert idx.shape[0] == m
      
    for i in xrange(0, m - 1):
        if not (i % 100):
            print i
        for j in xrange(i + 1, m):
            dist = jellyfish.jaro_winkler(titles[i], titles[j])
            if dist > threshold:
                id_i = idx[i]
                id_j = idx[j]
                if id_i not in clustered:
                    clustered[id_i] = (id_i, event_id, story_id)
                    story_id += 1
                if id_j not in clustered:
                    clustered[id_j] = (id_j, event_id, story_id)
                    story_id += 1
        else:
            story_id = 0
            event_id += 1
    
    idx_in_clustered = set(clustered.keys())
    idx = set(idx)
    
    left_idx = idx - idx_in_clustered
    for each in left_idx:
        clustered[each] = (each, event_id, story_id)
        event_id += 1
    
    return clustered

if __name__ == "__main__":
    from nltk import ConditionalFreqDist
    #===============================================================================
    # 初始输入
    #===============================================================================
#     fname = './io/bakeoff/1000_news_titles_contains_quotes.txt'
#     fname = './io/bakeoff/1000_news_titles_contains_quotes_with_id.txt'
#     fname = './io/test_v2/all_news_titles.txt'   
    fname = './io/bakeoff/all_news_titles_contains_quotes_with_id.txt'
    titles, idx = get_titles_and_idx(fname)
    titles, idx = titles[:10000], idx[:10000]
    
    #===============================================================================
    # 测试distance matrix函数
    #===============================================================================
#     dm = get_distance_matrix(titles, 0.9)
#     square_dm = squareform(dm)
#     print [(i+1,j+1) for i, row in enumerate(square_dm) for j, each in enumerate(row) if int(each) ==1]
#     pdb.set_trace()

    #===============================================================================
    # 测试aggregating
    #===============================================================================
    threshold = 0.96
    output_source = 'io/bakeoff/aggregator.pkl'
#     aggregator = aggregating(titles, idx, threshold)
#     clusters = [(event_id, id) for id, event_id, story_id in aggregator.values()]
#     cfd = ConditionalFreqDist(clusters)
#     
#     for event_id in cfd:
#         idx_in_a_group = cfd[event_id].keys()
#         if len(idx_in_a_group) > 1:
#             print idx_in_a_group
            
#     pdb.set_trace()
    
    # 存储aggregator的结果
#     save_cpickle(aggregator, output_source)
    
    #===============================================================================
    # 导入数据库
    #===============================================================================
    main(output_source)

'''
江海股份：薄膜电容器即将正式走向市场
江海股份：薄膜电容器即将正式走向市场

东兴证券：给予老板电器推荐评级
东兴证券：给予老板电器推荐评级
'''