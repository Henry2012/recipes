#-*- coding:utf-8 -*-

"""
#Name: Yi Jin
#Date: 6/24/2013
#Company: EverString
#File: eventClassifier.py
#Description: this class returns the event Classifier
"""

#import external python libraries
import nltk
import re
from pprint import pprint
from nltk import sent_tokenize
#import EverString python classes
import topicLib
from classifierLib import get_filtered_keywords

#---this class returns the event classifier---
class EventClassifier(object):
    #---initialization of the class---
    def __init__(self, trained_models_file):
        self.svm_classifier = topicLib.NewsClf(trained_models_file)

    #---classify based on the SVM method---
    def classify_svm(self, modify_sentence):
        svm_event = None
        event_type_list = [
                           "acquisition",
                           "beat_expectation",
                           "buyback",
                           "dividend",
                           "earning",
                           "key_hire",
                           "layoff",
                           "product_launch",
                           "product_price_cut",
                           "sales_record",
                           ]
        article_prediction_list = self.svm_classifier.clfConfArticle(modify_sentence)
        article_maximum = self.svm_classifier.clfArticle(modify_sentence)
        #---determine topic modeling classification based on threshold---
        threshold_min = 0
        if article_maximum == 0:
            if article_prediction_list[article_maximum] > threshold_min:
                svm_event = event_type_list[article_maximum]
        elif article_maximum == 1:
            if article_prediction_list[article_maximum] > threshold_min:
                svm_event = event_type_list[article_maximum]
        elif article_maximum == 2:
            if article_prediction_list[article_maximum] > threshold_min:
                svm_event = event_type_list[article_maximum]
        elif article_maximum == 3:
            if article_prediction_list[article_maximum] > threshold_min:
                svm_event = event_type_list[article_maximum]
        elif article_maximum == 4:
            if article_prediction_list[article_maximum] > threshold_min:
                svm_event = event_type_list[article_maximum]
        elif article_maximum == 5:
            if article_prediction_list[article_maximum] > threshold_min:
                svm_event = event_type_list[article_maximum]
        elif article_maximum == 6:
            if article_prediction_list[article_maximum] > threshold_min:
                svm_event = event_type_list[article_maximum]
        elif article_maximum == 7:
            if article_prediction_list[article_maximum] > threshold_min:
                svm_event = event_type_list[article_maximum]
        elif article_maximum == 8:
            if article_prediction_list[article_maximum] > threshold_min:
                svm_event = event_type_list[article_maximum]
        elif article_maximum == 9:
            if article_prediction_list[article_maximum] > threshold_min:
                svm_event = event_type_list[article_maximum]
        elif article_maximum == 10:
            if article_prediction_list[article_maximum] > threshold_min:
                svm_event = event_type_list[article_maximum]
        return svm_event

    #---classify the function---
    def classify(self, parsed_title, parsed_content_text):
        #---retrieve the title and content parsed sentence results---
        title_sent_results = parsed_title.get("sentences", None)
        content_sent_results = parsed_content_text.get("sentences", None)
        #---combine the title and first-second sentences of content---
        combined_sents = []
        for i, each_sent_dict in enumerate(title_sent_results):
            title_sent = each_sent_dict.get("tokens", None)
            if title_sent:
                combined_sents.append(title_sent)
        for i, each_sent_dict in enumerate(content_sent_results):
            if i <= 1:
                sent_sent = each_sent_dict.get("tokens", None)
                if sent_sent:
                    combined_sents.append(sent_sent)
        combined_sent_string = ""
        for each_sent_list in combined_sents:
            combined_sent_string += " " + " ".join(each_sent_list)
        #=======================================================================
        # print "title sentence: ", combined_sent_string
        # raw_input()
        #=======================================================================
        #---classify the event---
        svm_event = self.classify_svm(combined_sent_string)
        return [combined_sent_string, svm_event]


if __name__ == "__main__":

    #title = "Sony to cut 10,000 jobs"
    #content = "Sony to cut 10,000 jobs"

    title = "Activision Blizzard Earnings Beat Expectations"
    content = "Activision Blizzard beats earnings expectations as Call of Duty and Skylanders blast rival"
    trained_models_file = "/media/ebs0/Trained_Models/"
    comp_dict_file = "./input_files/comp_dict_2_6_2012_augmented.pkl"
    es_classifier = EventClassifier(trained_models_file)




