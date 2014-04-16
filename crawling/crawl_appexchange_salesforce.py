#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: crawling.crawl_appexchange_salesforce.py
Description: this program
Creation: 2013-11-28
Revision: 2013-11-28
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

import pdb
from bs4 import BeautifulSoup as BS
from lxml import html
from lxml.html import fromstring
from recipes import get_html


def _has_company_name(soup):
    a_soup = soup.a
    return bool(a_soup and
                a_soup.get('class', None) == 'tile-title' and
                '/listingDetail?listingId=' in a_soup.get('class', None))
    
if __name__ == "__main__":
    url_pattern = 'https://appexchange.salesforce.com/results?type=Services&sort=1&pageNo=%s&show=list'
    
    for i in range(1, 11):
        url = url_pattern % i
        html_text = get_html(url)
        print "gothere"
        soup = BS(html_text)
        for each in soup.find_all(_has_company_name):E
            print each
        raw_input()