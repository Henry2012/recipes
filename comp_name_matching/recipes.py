#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: company_name_matching.py
Description: this program
Creation: 2013-12-10
Revision: 2013-12-10
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

#===============================================================================
# Try the following methods:
# 1.  Match only the first word (that's not a stopword) of the company name
# 2.  Match n-1 words of the company name (for names > 1 word)
# 
# Don't forget to strip all punctuation at the beginning and end of each name token before you do the matching =>  stripped_token = re.sub(r'^([^\w]|_)*|([^\w]|_)*$','',token,re.UNICODE)
# 
# It's also not a bad idea to try accepting all news urls that have the same domain as the company, but check some of the results manually, especially for the news aggregator sites that we flagged before.
#===============================================================================

import re

def get_stopwords():
    stopwords = set()
    with open("english") as f:
        for line in f:
            if line.strip():
                stopwords.add(line.strip())
    return stopwords

def contains_company_name(comp_name, text):
    contains = False
    
    if comp_name.strip() in text:
        contains = True
    else:
        stripped_comp_name = re.sub(r'^([^\w]|_)*|([^\w]|_)*$', '',
                                    comp_name, re.UNICODE)
        if stripped_comp_name in text:
            contains = True
        else:
            stopwords = get_stopwords()
            split_comp_name = stripped_comp_name.split()
            
            first_non_stopword = None
            for i, word in enumerate(split_comp_name):
                if word not in stopwords:
                    first_non_stopword = word
                    break
            
            if word in text:
                contains = True
            elif " ".join(split_comp_name[:-1]) in text:
                contains = True
                
    return contains

if __name__ == "__main__":
    comp_name = ["TPS Technologies",
                 "Transform Software & Services"]

    text = ["""
We are pleased to announce that a new License Agreement has been signed between TPS TECH and SPIE Oil & Gas services, a subsidiary of the SPIE Group. SPIE is an international business delivering services to the oil and gas industries with headquarters in Europe, Africa, the Asian Pacific, and the Middle East.

 

SPIE_World.jpg

 

Part of the services-portfolio of SPIE is the treatment of oil waste including: incineration of liquid and solid waste, soil treatment, upgrading products, cleanup, decommissioning and rehabilitation of sites, and industrial cleaning (storage tanks, buildings, and offshore locations).   Now SPIE Africa will have the support of TPS TECH’s technology and remediation services in the following countries: Congo, Gabon, Angola, Nigeria and Lybia.

 

As SPIE Oil & Gas Services Africa offers a full range of products and services covering the entire oil chain spectrum, this license agreement offers great opportunities for both companies.
""",
    """
Denver, CO – May 6, 2013 – Transform Software and Services, the recognized leader in microseismic interpretation and analytic interpretation and modeling, today announced the impending commercial availability of TerraLocate.  Developed with a consortium of 8 leading unconventional E&P operators – TerraLocate has been specifically designed to meet industry needs for downhole microseismic monitored oil and gas wells.  Focused upon ensuring E&P operators receive optimal value from their microseismic investment – TerraLocate is the first microseismic event location system created by an independent software provider to directly connect with leading microseismic interpretation software and services."""]
    
    for c, t in zip(comp_name, text):
        print c in t
        print contains_company_name(c, t)