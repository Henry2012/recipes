#-*- coding:utf-8 -*-

import logging.handlers


def init_logger():
    LOG_FILENAME = 'logging.out'
    my_logger = logging.getLogger('MyLogger')
    my_logger.setLevel(logging.DEBUG)
    
    handler = logging.handlers.RotatingFileHandler(LOG_FILENAME,
                                                   mode='a',
                                                   maxBytes=200000,
                                                   backupCount=5)
    formatter = logging.Formatter('[%(levelname)s]\t[%(asctime)s]\t%(message)s',
                                  datefmt='%m/%d/%Y %I:%M:%S %p')
    
    handler.setFormatter(formatter)
    my_logger.addHandler(handler)
    
    return my_logger

if __name__ == '__main__':
    my_logger = init_logger()
    count_all_new_records = 1000
    
    for i in range(20):
        my_logger.debug('i = %d' % i)
        
    my_logger.debug('# of records onto MongoDB: %s' % count_all_new_records)
