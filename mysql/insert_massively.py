#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: mysql.transform_into_bulk_inserting.py
Creation: 2014-6-27
Revision: 2014-6-27
"""

#===============================================================================
# Functionalities:
#    1. add system variable settings
#    2. transform into bulk inserts
#===============================================================================

import pdb

def add_settings(file_handling, ):
    if 
    
def write_values(file_handling, values, prefix):
    #print type(values)
    #print len(values)
    values = ','.join(values)
    new_line = ' '.join([prefix, values, ';\n'])
    file_handling.write(new_line)
    
if __name__ == "__main__":
    PREFIX = 'INSERT INTO `analysis_idlink_va_elapsed` VALUES'
    N_PREFIX = len(PREFIX)
    bulk_in_1k = []
    with open('analysis_idlink_va_elapsed_10w_transformed.sql', 'w') as wf:
        with open('analysis_idlink_va_elapsed_10w.sql') as f:
            for i, line in enumerate(f):
                if i < 31:
                    wf.write(line)
                else:
                    if line.startswith(PREFIX):
                        value = line[N_PREFIX + 1:].rstrip(';\n')
                        bulk_in_1k.append(value)
                        
                    n_bulk_in_1k = len(bulk_in_1k)
                    if n_bulk_in_1k and not (n_bulk_in_1k % 1000):
                        #pdb.set_trace()
                        write_values(wf, bulk_in_1k, PREFIX)
                        bulk_in_1k = []
            else:
                write_values(wf, bulk_in_1k, PREFIX)