#-*- coding:utf-8 -*-

"""
#Name: Yi Jin
#Date: 8/12/2013
#Company: EverString
#File: entityMatcher.py
#Description: this class returns the entities (companies or tags) that matched from the article
"""

from common.basic_functions import get_stem, load_pickle
from pprint import pprint

#---this class returns the entities (companies or tags) that matched from the article---
class EntityMatcher(object):

    #---initialization of the class---
    def __init__(self, comp_dict_file, tag_dict_file):
        #define the dictionary of companies
        self.comp_dict = load_pickle(comp_dict_file)
        #=======================================================================
        # print "# of companies: ", len(self.comp_dict)
        # for each_key in self.comp_dict:
        #    print "key: ", each_key
        #    pprint(self.comp_dict[each_key])
        #    raw_input()
        #=======================================================================

        #define the dictionary of tags
        self.tag_dict = load_pickle(tag_dict_file)
        #=======================================================================
        # print "# of tags: ", len(self.tag_dict)
        # for each_key in self.tag_dict:
        #    print "key: ", each_key
        #    pprint(self.tag_dict[each_key])
        #    raw_input()
        #=======================================================================


    #---this function organizes the current input into a suitable input for match_entities---
    def input_api(self, pre_event_dict):
        #initialize output
        unknown_entity_dict = {
                                "unknown_companies": [],
                                "unknown_tags": []
                               }
        #retrieve relevant company list
        relevant_comp = pre_event_dict.get("relevant_comp", None)
        relevant_tag = pre_event_dict.get("relevant_tag", None)
        #assign to unknown_entity_dict---
        if relevant_comp and relevant_tag:
            unknown_entity_dict["unknown_companies"] = relevant_comp
            unknown_entity_dict["unknown_tags"] = relevant_tag
        #return output
        return unknown_entity_dict

    #---this function returns the matched entities---
    def match_entities(self, pre_event_dict):
        #define the input
        unknown_entity_dict = self.input_api(pre_event_dict)
        #initialize the output
        matched_entities_dict = {
                        "matched_companies": [],
                        "matched_tags": []
                        }
        #match companies
        matched_entities_dict["matched_companies"] = self.get_matched_companies(unknown_entity_dict["unknown_companies"])
        #match tags
        matched_entities_dict["matched_tags"] = self.get_matched_tags(unknown_entity_dict["unknown_tags"])

        pprint(matched_entities_dict)

        #return the output
        return matched_entities_dict

    #---this function returns the matched companies---
    def get_matched_companies(self, unknown_companies_list):
        #define output
        matched_companies = []
        #match the unknown companies to the company database
        for (comp_name, count) in unknown_companies_list:
            short_name = comp_name.lower()
            if short_name in self.comp_dict:
                matched_companies.append((self.comp_dict[short_name]["corp_id"], self.comp_dict[short_name]["comp_name"]))
        #return output
        return matched_companies

    #---this function returns the matched tags---
    def get_matched_tags(self, unknown_tags_list):
        #define output
        matched_tags = []
        #match the unknown tags to the tags database
        for (tag, count) in unknown_tags_list:
            stem_tag = get_stem(tag)
            if stem_tag in self.tag_dict:
                matched_tags.append((self.tag_dict[stem_tag]["tag_id"], self.tag_dict[stem_tag]["stemmed_tag"]))
        #return output
        return matched_tags

#---testing module---
if __name__ == "__main__":
    #define the tag and company dictionaries
    comp_dict_file = "./Input_Files/everstring_corp_info_1_20_2013.pkl"
    tag_dict_file = "./Input_Files/everstring_tag_dict_12_07_2012.pkl"
    #define the pre-event dictioanry
    pre_event_dict_file = "./Input_Files/test_news_dict.pkl"
    pre_event_dict = load_pickle(pre_event_dict_file)
    pre_event_dict["tag_list"]["unknown"].append(get_stem("cloud computing"))
    #===========================================================================
    # for each_key in pre_event_dict:
    #    print "keys: ", each_key
    #    pprint(pre_event_dict[each_key])
    #    raw_input("debug")
    #===========================================================================
    #initialize the class
    es_entity_matcher = EntityMatcher(comp_dict_file, tag_dict_file)
    #output the matched companies and tags
    matched_entities_dict = es_entity_matcher.match_entities(pre_event_dict)
    pprint(matched_entities_dict)








