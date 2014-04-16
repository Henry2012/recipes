#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
Creation: 2014-2-24
Revision: 2014-2-24
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

import cPickle
import datetime
import os
import pdb
import pytz
import re

from copy import copy
from commonregex import CommonRegex
from ConfigParser import SafeConfigParser
from collections import defaultdict
from dateutil.relativedelta import relativedelta
import dateutil.parser as parser
from mysqlAPI import Mysql

UPDATE_KEYS = ['entity_type', 'entity_name',
               'event_group', 'event_type', 'sub_event_type',
               'event_category', 'yahoo_code', 'processed',
               'event_id', 'event_novelty_score']

ALL_KEYS = ['entity_type', 'entity_name',
            'event_group', 'event_type', 'sub_event_type',
            'event_category', 'yahoo_code', 'processed',
            'title', 'abstract',
            'source', 'media_date',
            'event_id', 'event_novelty_score','content']

CURRENT_DIR = os.path.dirname(__file__)

# PARSER = SafeConfigParser()
# cfg_fname = 'db_and_event_keywords_and_fnames.cfg'
# cfg_fpath = os.path.join(CURRENT_DIR, cfg_fname)
# PARSER.read(cfg_fpath)

#===============================================================================
# 事件的强关键词
#===============================================================================

# STOCK_GAIN_KW = PARSER.get('stock-gain', 'keywords').split(',')
# PRODUCT_RELEASE_KW = PARSER.get('product-release', 'keywords').split(',')
# ACQUISITION_KW = PARSER.get('acquisition-completed-acquiree', 'keywords').split(',')

#===============================================================================
# 获取db相关的配置
#===============================================================================

def get_mysql(environ='production'):
    parser = get_db_parser()
    host = parser.get(environ, 'host')
    port = parser.getint(environ, 'port')
    user = parser.get(environ, 'user')
    pwd = parser.get(environ, 'pwd')
    dbname = parser.get(environ, 'dbname')

    mysql = Mysql(host, port, user, pwd, dbname)
    return mysql

def get_db_parser():
    db_cfg_fpath = os.path.join(CURRENT_DIR, 'db.cfg')
    parser = SafeConfigParser()
    parser.read(db_cfg_fpath)

    return parser

#===============================================================================
# 获取对应id的新闻时间 (media_date)
#===============================================================================

def get_all_fields(mysql, tbl_name):
    # 获得一张表的所有字段
    all_fields = []
     
    find_all_fields_sqlstr = '''
    SELECT COLUMN_NAME
    FROM information_schema.columns
    WHERE table_name = '%s'
    ORDER BY ORDINAL_POSITION
    asc;
    ''' % tbl_name
    
    for (each,) in mysql.find(find_all_fields_sqlstr):
        all_fields.append(each)
    return all_fields

def get_all_zhenquan_companies(mysql, company_tbl_name):
    zhenquan_companies = set()
    sqlstr = 'SELECT short_name from %s' % company_tbl_name + ' where short_name like "%证券%"'
    for (each,) in mysql.find(sqlstr):
        zhenquan_companies.add(each)
    return zhenquan_companies

def get_media_datetime(mysql, id, tname):
    find_sql = "select media_date from %s where id=%s" % (tname, id)
    return mysql.find(find_sql)[0][0]

#===============================================================================
# 获取对应id的新闻标题 (title)
#===============================================================================

def get_title(mysql, id, tname):
    find_sql = "select title from %s where id=%s" % (tname, id)
    return mysql.find(find_sql)[0][0]

#===============================================================================
# 获取文件名接口
#===============================================================================

# def get_fnames():
#     local_fnames = dict(PARSER.items('local_fnames'))
#     dir = local_fnames.pop('dir')
#     suffix = local_fnames.pop('suffix')
#
#     unconcerned_fname_indicators = set(['raw_fname',
#                         'stock_quote_fname',
#                         'stock_gain_fname',
#                         'non_stock_gain_fname',
#                         'product_release_fname',
#                         'non_product_release_fname',
#                         'acquisition_fname',
#                         'non_acquisition_fname',
#                         'analyst_ratings_fname',
#                         'non_analyst_ratings_fname',
#                         'init_event_id_fname',
#                         'stock_gain_event_distinction_fname',
#                         'analyst_ratings_event_distinction_fname'])
#
#     for indicator, fname in local_fnames.iteritems():
#         if indicator in unconcerned_fname_indicators:
#             new_fname = "".join([fname, suffix])
#         else:
#             new_fname = "".join(["records_with_", indicator[:-6], suffix])
#         fpath = os.path.join(dir, new_fname)
#         local_fnames[indicator] = fpath
#
#     return local_fnames

def get_stock_quotes(stock_quote_fname):
    with open(stock_quote_fname) as f:
        return set([line.strip() for line in f])

def get_stock_quote_mapping(mysql, company_tname):
    stock_quote_sqlstr = 'select short_name, symbol from %s' % company_tname
    stock_quote_mapping = {}
    for (short_name, symbol) in mysql.find(stock_quote_sqlstr):
#         if symbol.endswith('H'):
#             stock_quote_mapping[short_name] = symbol[:-1] + 'S'
#         else:
#             stock_quote_mapping[short_name] = symbol

        stock_quote_mapping[short_name] = symbol
    return stock_quote_mapping

def revise_ss_to_sh(mysql, news_comp_mapping_tname):
    find_sqlstr = "select id, symbol from %s" % news_comp_mapping_tname
    for i, (record_id, symbol) in enumerate(mysql.find(find_sqlstr)):
        if i and not (i % 100):
            print i
            mysql.commit()
        if symbol.endswith('S'):
            revised_symbol = symbol[:-1] + 'H'

            # execute update
            update_keys = ['symbol']
            update_values = [revised_symbol]
            upd_sqlstr = get_update_sqlstr(news_comp_mapping_tname, update_keys, update_values, record_id)
            mysql.execute(upd_sqlstr)
    else:
        mysql.commit()

def update_contains_zhengquan(mysql, stock_news_tname):
    upd_sql_fmt = 'update %s set contains_zhengquan=%s where id=%d'
    for i, (id, quotes) in enumerate(mysql.find('select id, quotes from %s where no_of_quotes>0' % stock_news_tname)):
        if i and not (i % 1000):
            print i
            mysql.commit()
        quotes = set(quotes.split('>|<'))
        updated_contains_zhengquan = int(contains_zhengquan(quotes))
        upd_sqlstr = upd_sql_fmt % (stock_news_tname, updated_contains_zhengquan, id)
        #print upd_sqlstr
        mysql.execute(upd_sqlstr)
    else:
        mysql.commit()
        
def update_contains_quote_before_colon(mysql, stock_news_tname):
    upd_sql_fmt = 'update %s set contains_quote_before_colon=%s where id=%d'
    for i, (id, title, quotes) in enumerate(mysql.find('select id,title,quotes from %s where no_of_quotes>0' % stock_news_tname)):
        if i and not (i % 1000):
            print i
            mysql.commit()
        quotes = set(quotes.split('>|<'))
        updated = int(contains_quote_before_colon(title, quotes))
        upd_sqlstr = upd_sql_fmt % (stock_news_tname, updated, id)
        #print upd_sqlstr
        mysql.execute(upd_sqlstr)
    else:
        mysql.commit()

def update_source(mysql, stock_news_tname):
    upd_sql_fmt = 'update %s set source=%s where id=%d'
    for i, (id, source) in enumerate(mysql.find('select id, source from %s' % stock_news_tname)):
        if i and not (i % 1000):
            print i
            mysql.commit()
        updated_source = source.strip()
        upd_sqlstr = upd_sql_fmt % (stock_news_tname, updated_source, id)
        mysql.execute(upd_sqlstr)
    else:
        mysql.commit()
        
def update_no_of_stories(mysql, stock_news_tname, stock_event_counts_tname):
    find_sqlstr = "select * from %s" % stock_event_counts_tname

    for i, (counter, event_id) in enumerate(mysql.find(find_sqlstr)):
        if not i:
            print "traversing stock_event_counts is done!!!"
        if i and not (i % 50):
            print i
            mysql.commit()
        #print counter, event_id
        upd_sqlstr = 'update %s set no_of_stories=%d where event_id=%d' % (stock_news_tname,
                                                                           counter,
                                                                           event_id)
        mysql.execute(upd_sqlstr)
    else:
        mysql.commit()

def update_is_news_comp_mapping_done(mysql, news_title_tname):
    find_null_sqlstr = 'select id from %s where is_news_comp_mapping_done is null' % news_title_tname
    upd_sqlstr_fmt = 'update %s set is_news_comp_mapping_done=1 where id=%d'
    for i, (id,) in enumerate(mysql.find(find_null_sqlstr)):
        if i and not (i % 1000):
            print i
            mysql.commit()
        mysql.execute(upd_sqlstr_fmt % (news_title_tname, id))
    else:
        mysql.commit()

def get_insert_and_update_sqlstr(tname, record_id, entity_name, company):
    #print ALL_KEYS
    keys_in_str = ','.join(ALL_KEYS)

    all_keys_copied = copy(ALL_KEYS)
    all_keys_copied[1] = "'%s'" % entity_name
    all_keys_copied[6] = "'%s'" % company
    updated_keys_in_str = ','.join(all_keys_copied)

    template = '''
    insert into %s (%s)
    select %s
    from %s
    where id=%s
    '''

    sqlstr = template % (tname, keys_in_str,
                         updated_keys_in_str, tname,
                         record_id)
    return sqlstr

def initiate_processed(mysql, tname):
    reinit_sqlstr = 'update %s set processed = null where processed is not null' % tname
    mysql.execute(reinit_sqlstr)
    mysql.commit()

def initiate_quotes(mysql, tname):
    reinit_sqlstr = 'update %s set quotes = null' % tname
    mysql.execute(reinit_sqlstr)
    mysql.commit()

def get_related_companies(title, stock_quotes):
    #===============================================================================
    # 存储出现股票名的index
    #===============================================================================
#     related_companies = defaultdict(list)
#     for quote in stock_quotes:
#         if quote in title:
#             idx = title.index(quote)
#             related_companies[quote].append(idx)

    #===============================================================================
    # 直接存储出现的股票名
    # stock_quotes可以是list,也可以是set.从performance角度上讲最好使用set类型。
    #===============================================================================
    related_companies = set()
    for quote in stock_quotes:
        if quote in title:
            related_companies.add(quote)

    #===============================================================================
    # 去除含有含有“证券”的股票名
    #===============================================================================
#     post_processed_companies = {}
#     if len(related_companies) > 1:
#         for each in related_companies:
#             if "证券" not in each:
#                 post_processed_companies[each] = stock_quotes[each]
#     else:
#         post_processed_companies = {each: stock_quotes[each] for each in related_companies}

    return related_companies

def get_update_values_for_most_keys(event_info, short_name, yahoo_code):
    some_values = list(event_info)

    update_values = []

    #pdb.set_trace()
    #print output[1]

    #entity_names = ">|<".join(output[1].keys())
    #companies = ">|<".join(output[1].values())

    update_values.append('COMP')
    update_values.append(short_name)
    update_values.extend(some_values)
    update_values.append(yahoo_code)
    update_values.append(1)
    return update_values

def get_update_values_for_some_keys(short_name, yahoo_code):
    update_values = []
    update_values.append(short_name)
    update_values.append(yahoo_code)
    return update_values

def get_update_sqlstrs(output, table_name, record_id):
    sqlstrs = []
    event_info = output[0]
    related_comp = output[1]

    if related_comp:
        if len(related_comp) > 1:
            print record_id
        for i, (short_name, yahoo_code) in enumerate(related_comp.iteritems()):
            if not i:
                update_values = get_update_values_for_most_keys(event_info, short_name, yahoo_code)
                upd_sqlstr_for_1st = get_update_sqlstr(table_name, UPDATE_KEYS, update_values, record_id)
                sqlstrs.append(upd_sqlstr_for_1st)
            else:
                upd_sqlstr_for_the_rest = get_insert_and_update_sqlstr(table_name, record_id, short_name, yahoo_code)
                sqlstrs.append(upd_sqlstr_for_the_rest)
    return sqlstrs

def get_update_sqlstr(table_name, update_keys, update_values, record_id):
    '''
    An example of the output for the current function is as follows:
    update event_alpha_copy
    set sub_event_type='completed', event_type='acquisition', entity_name='test', entity_type='COMP', yahoo_code='test', processed=1, event_category='acquisition-completed-acquiree', event_group='acquisitions-mergers'
    where id=628
    '''
    update_str = "update %s" % table_name

    set_str = []
    for key, value in zip(update_keys, update_values):
        if key == 'processed':
            set_str.append("%s=%d" % (key, value))
        elif (isinstance(value, basestring) and value):
            set_str.append("%s='%s'" % (key, value))
        elif isinstance(value, (int, long)):
            set_str.append("%s=%d" % (key, value))
        else:
            pass
            #print [key, value]
            #raise Exception('Unidentified types of value: %s' % str(value))

    set_str = ", ".join(set_str)
    set_str = "set " + set_str

    where_str = "where id=%d" % record_id

    sql_str = " ".join([update_str, set_str, where_str])
    return sql_str

def get_absolute_paths(fnames, dir_name):
    absolute_paths = []
    for fname in fnames:
        fpath = os.path.realpath(os.path.join(dir_name, fname))
        absolute_paths.append(fpath)
    return absolute_paths

def is_in_the_same_day_as(benchmark_dtime, evaluated_dtime):
    flag = False
    if benchmark_dtime.date() == evaluated_dtime.date():
        flag = True

    return flag

def is_in_the_same_period_as(benchmark_dtime, evaluated_dtime, time_period):
    '''
    time_period以天为基本单位
    '''
    flag = False
    difference = (benchmark_dtime.date() - evaluated_dtime.date()).days
    if abs(difference) < time_period:
        flag = True
    return flag

def save_cpickle(data_info, output_source):
    with open(output_source, 'wb') as wf:
        cPickle.dump(data_info, wf, -1)

def load_cpickle(fname):
    with open(fname, 'rb') as rf:
        output = cPickle.load(rf)
    return output

def get_init_event_id(init_event_id_fname):
    with open(init_event_id_fname) as f:
        return int(f.read().strip())

def update_init_event_id(updated_id, init_event_id_fname):
    with open(init_event_id_fname, 'w') as wf:
        wf.write(str(updated_id))

def get_largest_event_id(mysql):
    sqlstr = """select event_id from stock_news_copy
    ORDER BY event_id
    DESC
    limit 1"""
    return mysql.find(sqlstr)[0][0]

def validate(*fnames):
    flag = None
    if len(fnames) > 1:
        father, sons = fnames[0], fnames[1:]
        father_len = get_file_len(father)
        son_lens = sum(get_file_len(son) for son in sons)
        flag = (father_len == son_lens)
    else:
        raw_input('pls input at least 2 files')
    return flag

def get_file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def update_or_insert(mysql, tname, record_id):
    flag = None
    find_sqlstr = 'select processed from %s where id=%s' % (tname, str(record_id))
#     print find_sqlstr
#     print mysql.find(find_sqlstr)
#     raw_input()
    if mysql.find(find_sqlstr)[0][0]:
        flag = 'INSERT'
    else:
        flag = 'UPDATE'
    return flag

def contains_blank(title):
    return ' ' in title or '　' in title

def contains_colon(title):
    return "：" in title or ":" in title

def contains_hyphen(title):
    return "-" in title

def contains_zhengquan(quotes):
    # 只要有一个公司名中含有“证券”，则返回True
    flag = False
    if quotes:
        for quote in quotes:
            if "证券" in quote:
                flag = True
                break

    return flag

def contains_quote_before_colon(title, quotes):
    # 只要有一个公司名在第一个colon前，则返回True
    flag = False
    if quotes and contains_colon(title):
        for quote in quotes:
            if quote in title.split("：")[0]:
                flag = True
                break

    return flag

def count_lines(fpath):
    with open(fpath) as f:
        for i, line in enumerate(f):
            pass
    return i + 1

def count_records_in_db(mysql, tbl_name, first_day, last_day):
    # 返回时间区间为[first_day, last_day],并且
    # 信息源来自source的记录数量
    count = 0
    find_sqlstr = '''select source, media_date from %s
    where media_date between "%s" and "%s"
    order by media_date desc''' % (tbl_name, first_day, last_day)
    for i, (source, media_date) in enumerate(mysql.find(find_sqlstr)):
        if 'cs.com.cn' in source:
            count += 1
        if count == 1:
            print "The latest datatime: ", media_date

    print "# concerned records in db:", count
    return count

def count_months_and_records(crawler_output_dir):
    counter_for_months = 0
    counter_for_records = 0
    size_for_all = 0

    for fname in os.listdir(crawler_output_dir):
        fpath = os.path.join(crawler_output_dir, fname)
        fsize = os.stat(fpath).st_size

        # 针对所有爬取的文件得到相关的统计量
#         if fname.endswith('.txt') and "err" not in fname and fsize:
        # 只得到2014年爬取的文件统计量
        if (os.path.isfile(fpath) and
            fname.startswith('2014') and
            fname.endswith('.txt') and
            "err" not in fname and
            fsize):
            counter_for_months += 1
            counter_for_records += count_lines(fpath)
            size_for_all += fsize

    print "# all records: ", counter_for_records
    print "# months: ", counter_for_months
    print "# size of all the above files: ", size_for_all
    print

#===============================================================================
# datetime related functions
#===============================================================================

def contains_media_date_in_title(title, media_date_in_str):
    contains_flag = False
    
    dtimes = get_dtimes_from_title(title)
    
    media_dtime = transfer_str_to_date(media_date_in_str)
    year_in_media_dtime = media_dtime.year
    month_in_media_dtime = media_dtime.month
    day_in_media_dtime = media_dtime.day
    
    for dtime in dtimes:
        if dtime.year == 1900:
            if (dtime.month == month_in_media_dtime and
                dtime.day == day_in_media_dtime):
                 contains_flag = True
        else:
            if dtime == media_dtime:
                contains_flag = True
    return contains_flag

def get_dtimes_from_title(title):
    '''
    1. 从新闻标题中提取日期：
        - 08-5-26
        - 120708
        - 0708
    '''
    output_in_str = []
    output_in_dtime = []
    
    pattern1 = ur'[0-9]{6}'
    pattern2 = ur'[0-9]{4}'
    
    parse = CommonRegex(title)
    first_dates = parse.dates
    second_dates = re.findall(pattern1, title)
    third_dates = re.findall(pattern2, title)
    
    # 按次序提取str格式的时间
    output_in_str.extend(first_dates)
    if second_dates:
        output_in_str.extend(second_dates)
    else:
        output_in_str.extend(third_dates)

    # 将str格式的时间转化成datetime格式
    for date_in_str in output_in_str:
        if len(date_in_str) == 4:
            try:
                d = datetime.datetime.strptime(date_in_str, '%m%d')
                d.replace(year=1900)
                output_in_dtime.append(d)
            except ValueError, e:
#                 print e, date_in_str
                pass
        else:
            try:
                output_in_dtime.append(parser.parse(date_in_str, yearfirst=True))
            except ValueError, e:
#                 print e, date_in_str
                pass
        
    return output_in_dtime

def get_earliest_datetime(mysql, tname, date_field):
    find_sqlstr = '''
    select %s from %s
    ORDER BY %s
    ASC
    limit 1;
    ''' % (date_field, tname, date_field)

    return mysql.find(find_sqlstr)[0][0]

def get_latest_datetime(mysql, tname, date_field):
    find_sqlstr = '''
    select %s from %s
    ORDER BY %s
    DESC
    limit 1;
    ''' % (date_field, tname, date_field)

    return mysql.find(find_sqlstr)[0][0]

def get_monthly_interval(concerned_datetime):
    '''
    1. 首先判断关注的日期是否是一个月中的第一天
    2. 如果是，接着给出一个时间区间，类似于 ['2013-1-1', '2013-2-1'] (也可以是['2013-01-01', '2013-02-01'])
    '''
    # 得到当前月的第一天日期 (datetime)
    if concerned_datetime.day != 1:
        concerned_datetime = concerned_datetime.replace(day=1)
    first = concerned_datetime.date()

    # 得到下一月的第一天日期 (datetime)
    last = first + relativedelta(months=1)

    # 都转换成str
    return (first.strftime('%Y-%m-%d'),
            last.strftime('%Y-%m-%d'))

def get_weekly_interval(concerned_datetime):
    weekday = concerned_datetime.isoweekday()
    if weekday != 1:
        concerned_datetime = concerned_datetime - datetime.timedelta(days=(weekday - 1))
    first = concerned_datetime.date()

    last = first + relativedelta(weeks=1)
    return (first.strftime('%Y-%m-%d'),
            last.strftime('%Y-%m-%d'))

def update_weekly_interval(old_weekly_interval):
    new_first = transfer_str_to_date(old_weekly_interval[1])
    new_last = new_first + relativedelta(weeks=1)

    return (new_first.strftime('%Y-%m-%d'),
            new_last.strftime('%Y-%m-%d'))

def transfer_str_to_date(concerned_date_in_str):
    '''
    1. Convert datetime in string in the format "%Y-%m-%d %H:%M:%S" or "%Y.%m.%d %H:%M:%S"
    to datetime.datetime object with time set to zero.
    2. Example:
        input: "2014.12.13 13:00:00" or "2014-12-13 13:00:00"
        output: datetime.datetime(2014,12,13)
    '''
    d = parser.parse(concerned_date_in_str)
    return datetime.datetime(d.year, d.month, d.day)

def transfer_datetime_to_str(concerned_date_in_dtime, fmt='%Y-%m-%d %H:%M:%S'):
    return concerned_date_in_dtime.strftime(fmt)

def transfer_local_dtime_to_utc_dtime(local_dtime, local_tz='Asia/Shanghai'):
    local_tz = pytz.timezone(local_tz)
    local_dtime = local_tz.localize(local_dtime)
    utc_dtime = local_dtime.astimezone(pytz.utc)
    return utc_dtime

def transfer_local_dtime_str_to_utc_dtime_str(local_dtime_in_str, local_tz='Asia/Shanghai'):
    local_dtime = parser.parse(local_dtime_in_str)
    utc_dtime = transfer_local_dtime_to_utc_dtime(local_dtime)
    return transfer_datetime_to_str(utc_dtime)

if __name__ == "__main__":
    environ = 'local'
    mysql = get_mysql(environ)
    parser = get_db_parser()
    tbl_name = 'news_preprocessing_daily'
    company_tbl_name = 'company'
    
#     print mysql.find('select id from news_preprocessing_daily where id<3')
    update_contains_quote_before_colon(mysql, tbl_name)
    mysql.close()

#     titles = [u'    广发证券晨会纪要-140726',
#               u'    国金证券研究晨讯-120731',
#               u'    广发证券晨会纪要-0726',
#               u'    [长江证券]长江证券晨会纪要08-5-26',
#               u'    [海通证券]海通证券--晨会080526']
#     for title in titles:
#         print get_dtimes_from_title(title)
    
