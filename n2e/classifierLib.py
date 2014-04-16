#-*- coding:utf-8 -*-

"""
#Name: Yi Jin
#Date: 6/24/2013
#Company: EverString
#File: classifierLib.py
#Description: this class returns the event Classifier 
"""

#import external python libraries
import re
#import EverString python classes


def get_filtered_keywords():
    filtered_keywords = [
                                #fund raise
                                ["raise", "(.*) raise\\w{0,2} (\\$.*)", "fund_raise"],
                                ["seal", "(.*) seal\\w{0,2} (\\$.*)", "fund_raise"],
                                ["land", "(.*) land\\w{0,2} (\\$.*)", "fund_raise"],
                                ["ink", "(.*) ink\\w{0,2} (\\$.*)", "fund_raise"],
                                ["invest", "(.*) invest\\w{0,2} (\\$.*)", "fund_raise"],
                                ["secure", "(.*) secure\\w{0,1} (\\$.*)", "fund_raise"],
                                ["nab", "(.*) nab\\w{0,1} (\\$.*)", "fund_raise"],
                                ["get", "(.*) get\\w{0,1} (\\$.*)", "fund_raise"],
                                ["receive", "(.*) receive\\w{0,1} (\\$.*)", "fund_raise"],
                                
                                #personnel change
                                ["appoints", "\\bappoints\\b", "personnel_change"], 
                                ["hires", "\\bhires\\b", "personnel_change"],
                                ["name", "\\bname\\w{0,1} new\\b", "personnel_change"],
                                ["added", "\\badded\\b (.*) as (.*)", "personnel_change"],
                                
                                #product launches
                                ["debut", "debut\\w{0,3}", "product_launch"], 
                                ["introduce", "introduc\\w{0,3}", "product_launch"], 
                                ["intros", "\\bintros\\b", "product_launch"],
                                ["launch", "\\blaunch\\w{0,3}\\b", "product_launch"],
                                ["available", "\\bavailable\\b", "product_launch"],            
                                ["release", "\\brelease\\w{0,1}\\b", "product_launch"],
                                ["roll out", "\\broll\\w{0,2} out\\b", "product_launch"],
                                ["rolls out", "\\broll\\w{0,2} out\\b", "product_launch"],
                                ["unleash", "\\bunleash\\w{0,3}\\b", "product_launch"],
                                ["unveil", "\\bunveil\\w{0,3}\\b", "product_launch"],
                                
                                #ma transaction
                                ["acquire", "\\bacquire\\w{0,1}\\b", "ma_transaction"],
                                ["acquisition", "\\bacquisition\\w{0,1}\\b", "ma_transaction"],
                                ["buys", "\\bbuys\\b", "ma_transaction" ],
                                ["merge", "merge\\w{0,1} with", "ma_transaction"],
                                ["purchases", "\\bpurchases\\b", "ma_transaction"],
                                ["to buy", "\\bto buy\\b", "ma_transaction"],
                                               
                                #strategic partnership
                                ["agreement", "\\bagreement\\w{0,1} with\\b", "strategic_partnership"],
                                ["to collaborate on", "\\bcollaborate\\b", "strategic_partnership"], 
                                ["collaboration", "\\bcollaboration\\w{0,1}\\b", "strategic_partnership"], 
                                ["deal", "\\bdeal\\w{0,1} with\\b", "strategic_partnership"],
                                ["partner", "\\bpartner\\w{0,1} with\\b", "strategic_partnership"], 
                                ["partnership", "\\bpartnership\\w{0,1}\\b", "strategic_partnership"],
                                ["team", "\\bteam\\w{0,3} up\\b", "strategic_partnership"],    
       
                                #market research
                                ["industry", "\\bindustry .* forecast\\b", "market_research"],
                                ["industry", "\\bforecast .* industry\\b", "market_research"],
                                ["industry", "\\bindustry .* growth\\b", "market_research"], 
                                ["industry", "\\bgrowth .* industry\\b", "market_research"],
                                ["market", "\\bmarket .* forecast\\b", "market_research"], 
                                ["market", "\\bforecast .* market\\b", "market_research"],
                                ["market", "\\bmarket .* industry\\b", "market_research"], 
                                ["market", "\\bindustry .* market\\b", "market_research"],
                                ["market", "\\bmarket .* research\\b", "market_research"],
                                ["market", "\\bresearch .* market\\b", "market_research"],
                                ["market", "\\bmarket .* insights\\b", "market_research"],
                                ["market", "\\binsights .* market\\b", "market_research"],
                                ["market", "\\bmarket .* overview\\b", "market_research"],
                                ["market", "\\boverview .* market\\b", "market_research"],
                                ["research", "\\bresearch .* growth\\b", "market_research"],
                                ["research", "\\bgrowth .* research\\b", "market_research"],
                                ["sector", "\\bsector .* growth\\b", "market_research"],
                                ["sector", "\\bgrowth .* sector\\b", "market_research"],
                                #awards
                                ["award", "\\baward\\b", "awards"],
                                #conference
                                ["conference", "\\bconference\\b", "conference"], 
                                ["attend", "\\battend\\b", "conference"],
        ]
    #---define filtered_keywords---
    for i, (string_keyword, each_keyword, event_type) in enumerate(filtered_keywords):
        re_pattern = re.compile(each_keyword, re.IGNORECASE).search
        filtered_keywords[i].append(re_pattern)
    return filtered_keywords
    



