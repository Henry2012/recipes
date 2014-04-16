#-*- coding:utf-8 -*-

import datetime

def get_tier_type(each_news):
    return each_news['tier_type']
    
def get_event_type(each_news):
    return each_news['event_type']

def get_date_format_checked(date):
    '''
    '%Y-%m-%d %H:%M:%S' & '%Y-%m-%d'
    Sometimes the input 'date' is in "2012-06-26" format, while sometimes the date is in "2003-04-22 00:00:00" format.
    This function will convert both the above formats to datetime object.'''
    try:
        #create a datetime object
        date_time = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        #create string
        date_time.strftime('%Y-%m-%d %H:%M:%S')
    except:
        date_time = datetime.datetime.strptime(date, '%Y-%m-%d')
        date_time.strftime('%Y-%m-%d %H:%M:%S')
        
    return date_time

def merge_relevant_list(relevant_list, flag):
    '''relevant_list & tag here are merged lists with possible duplication. They are to be merged by deleting duplication,
    and getting the sum of scores.
    flag could be 'comp' or 'tag'
    '''
    temp_info = {}
    for flag_info in relevant_list:
        flag_id =  flag_info[flag + '_name']
        if temp_info.has_key(flag_id):
            temp_info[flag_id]['score'] += float(flag_info['score'])
        else:
            temp_info[flag_id] = flag_info
            temp_info[flag_id]['score'] = float(temp_info[flag_id]['score'])

    return temp_info.values()

def update_relevant_comp_and_tag(relevant_comp_in_mongo, new_relevant_comp, 
                                 tag_in_mongo, new_tag, updated_dict):
    relevant_comp = relevant_comp_in_mongo + new_relevant_comp
    tag = tag_in_mongo + new_tag
    
    updated_dict['relevant_comp'] = merge_relevant_list(relevant_comp, 'comp')
    updated_dict['relevant_tag'] = merge_relevant_list(tag, 'tag')
    return updated_dict

def cluster_based_upon_relevant_entities(relevant_comp_in_mongo, new_relevant_comp, 
                                         tag_in_mongo, new_tag, new_corp_id):
    #compare new_tag & tag_in_mongo
    tags_in_mongo = set([each['tag_id'] for each in tag_in_mongo])
    new_tags = set([each['tag_id'] for each in new_tag])
    tag_flag = bool(tags_in_mongo & new_tags)
    
    #compare relevant_comp_in_mongo & new_relevant_comp
    comps_in_mongo = set([each['corp_id'] for each in relevant_comp_in_mongo]) - set([new_corp_id])
    new_comps = set([each['corp_id'] for each in new_relevant_comp]) - set([new_corp_id])
    comp_flag = bool(comps_in_mongo & new_comps)
    
    return tag_flag & comp_flag