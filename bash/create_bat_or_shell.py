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
#     dir = args[1]

    dir = "screen_capture"
    #pattern = 'xvfb-run --server-args="-screen 0, 1024x768x24" ./CutyCapt --url=%s --out=%s/%s.png\n'
    #pattern = 'IECapt --silent --url=%s --out=%s/%s.png\n'
    pattern = 'phantomjs complex_screen_capture.js "%s" "%s.png"\n'
    with open("screen_capture_missing_ubuntu_v2.sh", "w") as wf:
        with open("../io/screenshotted_erroneous_phantomjs.txt") as f:
            for i, line in enumerate(f):
                if 3 >= i >= 0:
                    company_website, company_domain = line.strip().split("\t")
                    print company_website, company_domain
    #                 try:
    #                     p = subprocess.Popen("phantomjs screen_capture.js '%s' '%s.png'" % (company_website, company_domain))
    #                 except:
    #                     print "Error"
                    line = pattern % (company_website, company_domain)
                    wf.write(line)
