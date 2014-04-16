#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: sundries.test_ystockquote.py
Description: this program
Creation: 2014-1-2
Revision: 2014-1-2
"""

__version__ = '0.2.5dev'

try:
    # py3
    from urllib.request import Request, urlopen
    from urllib.parse import urlencode
except ImportError:
    # py2
    from urllib2 import Request, urlopen
    from urllib import urlencode

def _request(symbol, stat):
    url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (symbol, stat)
    req = Request(url)
    resp = urlopen(req)
    content = resp.read().decode().strip()
    return content

if __name__ == "__main__":
    
    symbol = "600180.SS"
    stat = \
        'ydb2r1b3qpoc1d1cd2c6t1k2p2c8m5c3m6gm7hm8k1m3lm4l1t8w1g1w4g3p' \
        '1g4mg5m2g6kvjj1j5j3k4f6j6nk5n4ws1xj2va5b6k3t7a2t615l2el3e7v1' \
        'e8v7e9s6b4j4p5p6rr2r5r6r7s7'
        
    _request(symbol, stat)