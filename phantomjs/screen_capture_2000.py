#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: phantomjs.screen_capture.py
Description: this program
Creation: 2013-11-26
Revision: 2013-11-26
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

import subprocess
import sys

if __name__ == "__main__":
#     args = sys.argv
#     
#     start = args[1]
#     end = args[2]
    
    with open("../io/3k_company_websites_and_domains.txt") as f:
        for i, line in enumerate(f):
            if 2199 >= i >= 2000:
                company_website, company_domain = line.strip().split("\t")
                print company_website, company_domain
                try:
                    p = subprocess.Popen("phantomjs screen_capture.js '%s' '%s.png'" % (company_website, company_domain))
                except:
                    print "Error"