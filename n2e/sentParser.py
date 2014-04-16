#-*- coding:utf-8 -*-

"""
#Name: Yi Jin and Hua Gao
#Date: 7/2/2013
#Company: EverString
#File: sentFilter.py
#Description: this class filters the sentences within the article
"""

#import reference files
import sys
from pprint import pprint
from pymongo import Connection

#import EverString reference files
from corenlp import StanfordCoreNLP


reload(sys)
sys.setdefaultencoding("utf8")


#---this class returns the parsed sentence---
class SentParser(object):
    #---initialization of the class---
    def __init__(self, config):
        self.nlp = StanfordCoreNLP(config)

    #---parse the title and content---
    def parse(self, title, content):
        temp_dict = {
                        "title": title,
                        "content": content
                     }
        parsed_results = self.nlp.processNewsArticle(temp_dict)
        parsed_errors = parsed_results.get("parseErrors", None)
        title_dict_results = None
        sentence_dict_results = None
#        if parsed_errors >= 0:
#            title_dict_results = parsed_results.get("titleResults", None)
#            sentence_dict_results = parsed_results.get("articleResults", None)
        #---return title_dict_results and sentence_dict_results---
        return parsed_results

if __name__ == "__main__":
    #---prepare the test records---
    es_db = es_db = Connection("ec2-107-22-30-103.compute-1.amazonaws.com")
    es_records = es_db.esdb.event_news.find()
    #prepare company dict file
    comp_dict_file = "./input_files/comp_dict_2_6_2012_augmented.pkl"
    #---initialize the SentParser() class---
    es_sentParser = SentParser(comp_dict_file)
    #---testing the records---
    for each_record in es_records:
        #get title and content_text
        title = each_record.get("title", None)
        content_text = each_record.get("content_text", None)
        #if title and content_text exist
        if title and content_text:
            parsed_results = es_sentParser.parse(title, content_text)



