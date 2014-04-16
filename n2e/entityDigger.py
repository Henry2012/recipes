#-*- coding:utf-8 -*-

"""
#Name: Yi Jin
#Date: 6/24/2013
#Company: EverString
#File: sentFilter.py
#Description: this class filters the sentences within the article
"""
#import external python libraries
import nltk
from pprint import pprint
#import EverString python classes
from common.basic_functions import get_complete_tokens, get_cap_count, get_stopwords

#---this class returns the potential entities---
class EntityDigger(object):
    #---initialization of the class---
    def __init__(self):
        self.stopwords = get_stopwords()

    #---dig for potential company and tags---
    def dig(self, parsed_title_dict, parsed_content_dict):
        [content_unknown_comp_list, content_unknown_tag_list] = self.dig_content(parsed_content_dict)
        return [content_unknown_comp_list, content_unknown_tag_list]

    #---get cap count---
    def get_cap_status(self, phrase_tokens):
        cap_count = 0
        for each_word in phrase_tokens:
            for each_letter in each_word:
                if each_letter.isupper():
                    cap_count += 1
                    break
        cap_status = False
        if cap_count == len(phrase_tokens):
            cap_status = True
        return cap_status

    #---get lower count---
    def get_lower_status(self, phrase_tokens):
        cap_count = 0
        for each_word in phrase_tokens:
            for each_letter in each_word:
                if each_letter.isupper():
                    cap_count += 1
                    break
        low_status = True
        if cap_count > 0:
            low_status = False
        return low_status


    #---dig for potential company and tags in company---
    def dig_content(self, parsed_content_dict):
        #---define company and tag lists---
        [content_unknown_comp_list, content_unknown_tag_list] = [ [], [] ]
        #---retrieve parsed results and the noun phrases
        noun_phrase = []
        sentence_dict = parsed_content_dict.get("sentences", None)
        if sentence_dict:
            for each_sent_dict in sentence_dict:
                tokens_list = each_sent_dict.get("tokens", None)
                parseTree_list = each_sent_dict.get("parseTree", None)
                dep_list = each_sent_dict.get("dependencies", None)
                pos_list = each_sent_dict.get("posTags", None)
                if tokens_list and dep_list:
                    for (rel, gov_i, dep_i) in dep_list:
                        if rel == "nn":
                            string_token = " ".join([tokens_list[dep_i], tokens_list[gov_i]])
                            noun_phrase.append(string_token)
                        elif rel == "nsubj":
                            noun_phrase.append(tokens_list[dep_i])
        #---separate into unknown_comp_list and unknown_tag_list---
        for each_phrase in noun_phrase:
            phrase_tokens = each_phrase.split()
            if self.get_cap_status(phrase_tokens):
                modify_phrase = each_phrase.replace("_", " ")
                content_unknown_comp_list.append(each_phrase)
            elif len(phrase_tokens) >= 2 and self.get_lower_status(phrase_tokens):
                content_unknown_tag_list.append(each_phrase)
        #---perform frequency distribution---
        content_unknown_comp_list = nltk.FreqDist(content_unknown_comp_list).items()
        content_unknown_tag_list = nltk.FreqDist(content_unknown_tag_list).items()

        return [content_unknown_comp_list, content_unknown_tag_list]


