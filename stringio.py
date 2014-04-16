#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: stringio.py
Description: this program provides efficient string concatenation
Creation: 2013-11-19
Revision: 2013-11-19
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

#===============================================================================
# Reference: http://stackoverflow.com/questions/4330812/how-do-i-clear-a-stringio-object
# Don't bother clearing it, just create a new one—it’s faster.
# So i don't have to use truncate method
#===============================================================================

def concatenate_strings():
    from cStringIO import StringIO
    file_str = StringIO()
    for num in xrange(10):
        file_str.write(`num`)
    
    return file_str.getvalue()

if __name__ == "__main__":
    print concatenate_strings()