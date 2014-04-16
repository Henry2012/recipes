#-*- coding:utf-8 -*-

"""
#Name: Yi Jin
#Date: 7/20/2013
#Company: EverString
#File: sentFilter.py
#Description: this class filters the sentences within the article
"""

import nltk
from pymongo import Connection

#---this class returns the filtered sent---
class SentFilter(object):

    #---initialization of the class---
    def __init__(self):
        [self.title, self.content_text] = [None, None]

    #---filter the title---
    def filter_title(self, title):
        modify_title = title
        try:
            modify_title = modify_title.encode("ascii", "ignore").encode("utf-8")
        except:
            modify_title = modify_title.decode("ascii", "ignore").encode("utf-8")
        return modify_title

    #---filter the content_text
    def filter_content_text(self, content_text):
        modify_content_text = content_text
        for each_pattern in ["\n"]:
            try:
                modify_content_text = modify_content_text.encode("utf-8").decode("ascii", "ignore").replace(each_pattern, " ")
            except:
                modify_content_text = modify_content_text.decode("ascii", "ignore").encode("utf-8").replace(each_pattern, " ")
        #extract only the first 3 sentences of the content
        modify_content_sents = nltk.sent_tokenize(modify_content_text)
        modify_content_text = " ".join(modify_content_sents[:3])
        return modify_content_text

    #---filter the title and content_text
    def filter(self, title, content_text):
        modify_title = self.filter_title(title)
        modify_content_text = self.filter_content_text(content_text)
        return [modify_title, modify_content_text]

if __name__ == "__main__":
    #---initilialize the SentFilter()---
    es_sentFilter = SentFilter()
    #---prepare es records---
    news_records = Connection("ec2-107-22-30-103.compute-1.amazonaws.com").esdb.event_news.find()
    for i, each_record in enumerate(news_records):
        title = each_record.get("title", None)
        content_text = each_record.get("content_text", None)
        if title and content_text:
            [modified_title, modified_content_text] = es_sentFilter.filter(title, content_text)
            print i
            print "modified title: ", modified_title
            print "modified content text: ", modified_content_text
            print "\n"
        if i == 100:
            break

