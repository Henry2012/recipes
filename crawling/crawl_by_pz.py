# -*- coding: utf-8 -*-
# Author: Peng Zhuo
# Copyright: EverString
# Date:
# Distributed under terms of the EverString license.

import ConfigParser
#import mechanize
import urllib2
import BeautifulSoup
import cookielib


if __name__ == '__main__':
    output = open('result2.txt','r')
    wf = open('name_domain.txt', 'w')
    i = 0
    #browser = mechanize.Browser()
    #cj = cookielib.LWPCookieJar()
    #browser.set_cookiejar(cj)
    #browser.set_handle_equiv(True)
    #browser.set_handle_redirect(True)
    #browser.set_handle_referer(True)
    #browser.set_handle_robots(False)
    for line in output:
        i = i+1
        if i <= 145:
            continue

        tokens = line.strip().split('    ')
        url_part = tokens[0]
        name = tokens[1]

        response = urllib2.urlopen("https://appexchange.salesforce.com" + url_part)
        text = response.read()
        soup = BeautifulSoup.BeautifulSoup(text)
        link = soup.find('a',id="learnmore")
        try:
            if link is not None:
                print link.get('href')
                wf.write(name + '\t' + link.get('href') + '\n')
        except:
            pass
        #for each in soup.findAll('a[id="learnmore"]'):
        #    try:
        #        if each.get('id') == "learnmore":
        #            print each.get('href')
        #            wf.write(name +'\t' + each.get('href') + '\n')
        #    except:
        #        pass
