#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: news_stat.page_types.py
Description: this program gives a list of page types in webpage collection
Creation: 2014-1-4
Revision: 2014-1-4
"""

# # of elements: 26
PAGE_TYPES = [
        "About",
        "Contact",
        "News",
        "Blog",
        "Product",
        "Overview",
        "Job",
        "Sitemap",
        "Mobile",
        "Login",
        "Award",
        "Partner",
        "Pricing",
        "Team",
        "Event",
        "Language",
        "LearnMore",
        "Help",
        "Investor",
        "Cart",
        "Client",
        "Corporate",
        "Legal",
        "Webinar",
        "Tour",
        "GetStarted"]

if __name__ == "__main__":
    with open("../io/test.txt", "w") as wf:
        for each in PAGE_TYPES:
            wf.write(each + "\t")