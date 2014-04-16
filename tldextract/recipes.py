#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: tldextract.recipes.py
Description: this program
Creation: 2013-11-26
Revision: 2013-11-26
"""

import tldextract

#===============================================================================
# ExtractResult(subdomain='www', domain='gc1', suffix='com')
# ExtractResult(subdomain='', domain='gc1', suffix='com')
# ExtractResult(subdomain='', domain='gc1', suffix='com')
#===============================================================================

urls = ["www.gc1.com",
        "gc1.com",
        "gc1.com/",
        "helpinghand.com.au/",
        'http://bangbang.qq.com/web/poster/robot1.htm',
        'http://cache.tv.qq.com/bigportal/index.html']

for url in urls:
    s = tldextract.extract(url)
    domain = '.'.join([s.domain, s.suffix])
    print domain
raw_input()

#===============================================================================
# 预处理公司的websites,统一转换成http://www.sysatl.com的格式
# 1. http://www.sysatl.com/ --> http://www.sysatl.com
# 2. www.sysatl.com/home --> http://www.sysatl.com
#===============================================================================

# with open("../io/3k_company_websites_updated.txt", "w") as wf:
#     with open("../io/3k_company_websites.txt") as f:
#         for line in f:
#             # 去除最后的"/"
#             line = line.rstrip().rstrip("/")
#             # 只需要首页面
#             if ("http://" not in line and
#                 "/" in line):
#                 slash_index = line.find("/")
#                 line = line[:slash_index]
#             # 加上协议
#             if line.find("http://") != 0:
#                 line = "http://" + line
#                 wf.write(line + "\n")

#===============================================================================
# 为websites生成domains
#===============================================================================

with open("../io/3k_company_websites_and_domains.txt", "w") as wf:
    with open("../io/3k_company_websites_updated.txt") as f:
        for line in f:
            company_website = line.strip()
            s = tldextract.extract(company_website)
            company_domain = '.'.join([s.domain, s.suffix])
            new_line = "\t".join([company_website, company_domain])
            wf.write(new_line + "\n")
