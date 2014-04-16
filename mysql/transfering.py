# -*- coding: utf-8 -*-

'''
Created on 2013-8-2

@author: Qiqun.H

Functionalities:
- add logging modules
- add cfg for database, log_fname, and log_of_logs filename
- check whether a file exists
- add date argument for transfering logs on any day
    cmd: python transfering.py develop 2013-09-23
- solve issues resulting from a tricky trap in producing log filename:
    1. Unless there'r logs for a new day, then the log file is a name
    without date.
    2. Every record in one log file has the same date.
'''
import MySQLdb
import datetime
from ConfigParser import SafeConfigParser
#from pprint import pprint
import sys
import logging.handlers
import os

class Context(object):
    def __init__(self):
        self.environment = sys.argv[1]
        
        self.log_parser = SafeConfigParser()
        self.log_parser.read('log.cfg')
        
        self.db_parser = SafeConfigParser()
        self.db_parser.read('db.cfg')
        
    def get_my_logger(self):
        # Here returns an instance for a logger
        LOG_FILENAME = self.log_parser.get(self.environment, 'log_of_logs')
        return init_logger(LOG_FILENAME)
    
    def get_prefix(self):
        # get the prefix for every galaxy log file
        # %(path)s/galaxy-track.log.
        prefix = self.log_parser.get(self.environment, 'prefix')
        return prefix
        
    def get_db_cfg(self):
        db_cfg = dict(self.db_parser.items(self.environment))
        
        db_cfg['port'] = int(db_cfg['port'])

        return db_cfg
    
    def get_date(self):
        if len(sys.argv) == 3:
            # str like "2013-09-18"
            date = sys.argv[-1]
        else:
            date = get_yesterday()
            
        return date
    
    def get_galaxy_log_fname(self):

        wrapper = self.get_prefix()
        date = self.get_date()
        #print wrapper, date
        return wrapper + date


class LogTransfered(object):
    HEADER = '---Start transfering---'
    NON_EXISTING_FILE = "[ERROR: %s]This file '%s' doesn't exist!"
    TRANSFERED_ALREADY = "[ATTENTION: %s]Log with the required date has been transfered."
    TRANSFERED_STAT = "[INFO: %s] # of records transfered: %s"
    EXCEPTION = "[ERROR] Exceptions captured: %s"
    FOOTER = '----Transfering done---'
    
    def __init__(self):
        self.context = Context()
        self.my_logger = self.context.get_my_logger()
        self.date = self.context.get_date()
        self.galaxy_log_fname = self.context.get_galaxy_log_fname()
        
        db_cfg = self.context.get_db_cfg()
        self.table = db_cfg.pop('table')
        self.conn = MySQLdb.connect(**db_cfg)
        self.cur = self.conn.cursor()
        self.keys = get_keys()
        
    def is_exist(self, date):
        # Decide whether a record with a given date
        # exist in db
        is_exist_query = get_isexist_query(date, self.table)
        self.cur.execute(is_exist_query)
        flag = self.cur.fetchall()[0][0]
        
        return flag

    def insert_record(self, record):
        values = [string2varchar(self.conn, str(elem)) for elem in record]
        
        insert_query = get_insert_query(self.table, self.keys, values)

        self.cur.execute(insert_query)
        self.conn.commit()

        return len(record)

    def transfered(self):
        #print self.galaxy_log_fname
        if os.path.isfile(self.galaxy_log_fname):
            records = get_records(self.galaxy_log_fname)

            if records:
                flag = self.is_exist(self.date)
                if not flag:
                    for record in records:
                        self.insert_record(record)
                    output = self.TRANSFERED_STAT % (self.date, len(records))
                else:
                    output = self.TRANSFERED_ALREADY % (self.date)
        else:
            prefix = self.context.get_prefix().rstrip('.')
            if os.path.isfile(prefix):
                records = get_records(prefix)
                
                one_record = records[0]
                date = one_record[-1]
                date = date.split(' ')[0]
                if date == self.date:
                    flag = self.is_exist(date)
                    if not flag:
                        for r in records:
                            self.insert_record(r)
                        output = self.TRANSFERED_STAT % (date, len(records))
                    else:
                        output = self.TRANSFERED_ALREADY % (date)
                else:
                    output = self.NON_EXISTING_FILE % (self.date, self.galaxy_log_fname)
                    
            else:
                output = self.NON_EXISTING_FILE % (self.date, prefix)
        
        return output

    def add_log(self):
        self.my_logger.debug(self.HEADER)
        try:
            output = self.transfered()
            self.my_logger.debug(output)
        except Exception, e:
            self.my_logger.debug(self.EXCEPTION % e)
        finally:
            self.my_logger.debug(self.FOOTER)


def get_isexist_query(date, table):
    return '''SELECT EXISTS(SELECT id FROM %s
              WHERE DATE(date)="%s")''' % (table, date)


def get_insert_query(table, keys, values):
    return ("insert into %s (%s) values (%s)" %
            (table, ", ".join(keys), ", ".join(values)))


def init_logger(LOG_FILENAME):
    my_logger = logging.getLogger('MyLogger')
    my_logger.setLevel(logging.DEBUG)
    
    handler = logging.handlers.RotatingFileHandler(LOG_FILENAME,
                                                   mode='a',
                                                   maxBytes=200000,
                                                   backupCount=2)
    formatter = logging.Formatter('[%(levelname)s]\t[%(asctime)s]\t%(message)s',
                                  datefmt='%m/%d/%Y %I:%M:%S %p')

    handler.setFormatter(formatter)
    my_logger.addHandler(handler)

    return my_logger


def get_records(fname):
    records = []

    with open(fname) as f:
        for line in f:
            values = get_values(line)
            records.append(values)

    return records


def get_values(record):
    elements = record.split(' - ')

    # Output: '2013-07-29 11:24:38.987'
    date = elements[0]

    # Output: '2013-07-29 11:24:38'
    #date = elements[0].split('.')[0]

    sub_elements = elements[1].split(';')

    user_browser = sub_elements[0].split(':')
    user = user_browser[0]
    browser = user_browser[1]

    actions = sub_elements[1]
    split_actions = actions.split(',')
    action = split_actions[0]
    info = split_actions[1].strip()

    values = [user, action, info, browser, date]

    return values


def get_keys():
    return ['user', 'action',
            'info', 'browser', 'date']


def get_yesterday():
    # Output: yesterday in str format "2013-09-18"
    today = datetime.datetime.today()
    one_day = datetime.timedelta(days=1)
    yesterday = today - one_day

    # Output: required format for identifying yesterday's log file
    #yesterday = yesterday.strftime("%Y-%m-%d %H:%M:%S")
    yesterday = yesterday.strftime("%Y-%m-%d")

    return yesterday


def string2varchar(conn, string):
    return conn.literal(string)


if __name__ == "__main__":
    log_transfered = LogTransfered()
    log_transfered.add_log()

    #context = Context()
    #print context.get_galaxy_log_fname()
