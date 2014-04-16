#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: crawling.extracter.py
Description: this program
Creation: 2013-11-29
Revision: 2013-11-29
"""

from lxml.html import fromstring

def get_href(html):
    doc = fromstring(html)
    return doc.xpath('//a/@href')

def get_script(html):
    extracted = []
    doc = fromstring(html)
    for each in doc.xpath('//script'):
        script_text = each.text
        if script_text:
            extracted.append(script_text)
    return extracted

if __name__ == "__main__":
    
    with open("../io/sample_1.html") as f:
        html = f.read()
        
    print get_href(html)
    print get_script(html)