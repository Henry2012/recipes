# -*- coding: utf-8 -*-

'''
Created on 2013-5-28

@author: QQ.Han
@module: grab_weather_underground_data.test.test_day_temp

Test ways to retrieve the daily temperature
'''

import urllib2
from bs4 import BeautifulSoup

def has_attr_class(tag):
    '''
    find tags with "class" as an attribute'''
    return tag.name == "span" and tag.has_attr('class')

def get_mean_temp(url):
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    
    # <class 'bs4.BeautifulSoup'>
    #print type(soup)
    
    history_table = soup.find("table", id="historyTable")
    
    # <class 'bs4.element.Tag'>
    #print type(history_table)
    
    mean_temp = history_table.find_all("span", class_="b")[0].string
    
    return mean_temp

def test_string_text(url):
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    return soup.string, soup.text

if __name__ == "__main__":
    from pprint import pprint
    
    url = "http://www.wunderground.com/history/airport/KBUF/2000/1/1/DailyHistory.html"
    print get_mean_temp(url)
    
    pprint(test_string_text(url))
    