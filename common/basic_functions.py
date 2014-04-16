#-*- coding:utf-8 -*-

import json
import pickle
import re
import nltk
import os
from pprint import pprint

from nltk import *
from nltk.corpus import stopwords
from datetime import date
#----------------------------------------------------------------------------------------------
#----------Basic Functions---------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
def load_json_line(filename):
    of = open(filename,'r')
    for line in of:
        yield json.loads(line.strip())
    of.close()
    
def clean_stopwords(sentence):
    tuple_list = []
    nlp_stopwords = get_stopwords()
    
    sentence = sentence.lower().split()
    ref_set = set(sentence)
    for i, each_token in enumerate(sentence):
        if each_token in nlp_stopwords:
            sentence[i] = ">|<"
    sentence = " ".join(sentence)        
    tuple_list = re.split(">|<", sentence)
    tuple_list = [x.strip(' ') for x in tuple_list]
    tuple_list = [x.strip('|') for x in tuple_list]  
    tuple_list = filter(None, tuple_list)
    tuple_list = " ".join(tuple_list)
    list_tuple_list = tuple_list.split()
    ref_tuple = set(list_tuple_list)
    #print ref_set, ref_tuple
    #print ref_tuple.intersection(ref_set)
    if ref_tuple.intersection(ref_set) != ref_set:
        list_tuple_list = []
    return list_tuple_list

def get_stopwords():
    nltk_stopwords = stopwords.words("english")
    user_defined_stopwords = [
                              ",", "$", "(", ")", "<", ">", "[", "]", '"', "'", ";", ":", "#", "@", "!", "*", "&", "%", "/", "-", "--", ".", "''", "new" 
                              "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", 
                              "month", "day", "year", "week", "yesterday", "second", "minute", "hour",
                              "january", "feburary", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december",
                              "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sept", "sep", "oct", "nov", "dec",
                              "{", "}", "+", "//",
                              "first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth",    
                              "world", "latest", "version", "need", "another", "early", "enhance", "enhanced", "every", "following", "follow",
                              "get", "go ", " go", "good", "great", "large", "like", "addition", "award winning", "little", "million",
                              "miss", "next generation", "next-generation", "last", "north america", "north", "south", "old", "beta",
                              "quarter", "edition", "better", "best", "son", "east", "west", "firm", "partner", "channel", "united states",
                              "fund", "leading", "next-generation", "next generation", "company", "products", "provides", "services", "service", "design", "development",
                              "allows", "held", "new", "york", "san", "francisco", "provider", "global", "based", "next", "small", "time", "http", 
                             ]
    overall_stopwords = nltk_stopwords + user_defined_stopwords
    return overall_stopwords

def get_stopwords_for_company():
    nltk_stopwords = stopwords.words("english")
    user_defined_stopwords = [
                             #A
                            "action","ad","artist", "awareness", "Automotive industry", "A", "A Company", "AB", "AC", "Active", "ADVANCED MEDIA",
                            "Advanced Technology",    "AIR", "AL", "ALL", "Alumni", "Android", "Animal", "Ape", "APRIL", "As", "Assist", "Australia",
                            "Author", "Awesome", "auditorium", "anthony", "alliance", "address", "app", "automotive", "applied system", "about", 
                            "audience", "all media guide", "ambassador", "adaptive", "all covered", "ant", "act", "advertising.com", "advertising",
                            "automatic", "access", "affinity", "Aerospace", 
                            #B
                            "blog", "buddy", "Ben", "BEST", "Between", "Blind", "BLUE", "Books", "Box", "Brain", "Bridge", "Broadcast", "Bus",
                            "Business Consultants", "bank", "billy", "business solution", "bank", "bill", "better", "bundle", "beyond", "base",
                            "become", "barcode", "blogs", "boom", "beach", "booking", "backstage", "business", "business.com", "business", "born.com", "born",
                            "backcountry",
                            #C
                            "center", "ces", "chairman", "china", "C", "CA", "Cafe", "CAN", "Capital", "Card", "Challenge", "Cherry", "Chess", "CHOICE",
                            "Club Website", "Co", "CODE", "College", "Company", "Connect", "CORE", "Create", "Cross", "CUT", "computer services", "closer", "cloud",
                            "composite", "composite software", "content", "cast", "connected", "cable", "cars", "co-founder", "credit", "comedy", "candy",
                            "collective", "current", "compass", "chill", "choose", "chat", "compute", "cloudy", "coastal.com", "coastal", "compete",
                            "chicago.com", "chicago", "city", "city.com", "Care", "cfo", "case",
                            #D
                            "digital","digital media", "D", "December", "Design", "Desk", "Develop", "Director", "Directors", "Discovery", "Division",
                            "Domain Registration", "Drive", "deliver", "data management", "data integration", "do", "data recovery", "daydream", "disco", 
                            "ditto", "debt", "dns", "dec", "delivery", "delivery.com", "dog", "Dog.com", "diamond", "director of marketing", 
                            #E
                            "east", "edt", "enterprise", "Education", "Elements", "Energy", "Engage", "EU", "Exceptional", "Expand", "Explorer", "expression",
                            "edge", "examiner" "elevate", "election", "entreprenuer", "expo", "expert", "Equities", "elastic" 
                            #F
                            "fabric", "far", "FACE", "Family", "FAST", "Fine", "Firm", "FIRST", "Five", "FORM", "Forty", "Foundation", "Franklin", "Free", 
                            "Front", "Fuel", "fan", "fogs", "financial institution", "federal", "fitness", "founder", "force", "feedback", "focus",  
                            "fry", "found", 
                            #G
                            "green", "group", "GAME", "Gate", "George", "Global", "Go", "GOOD", "guru", "grow", "get", "gmt", "good thing", "gifts", "giftcards",
                            "genius", "gomez", "giving", "gameplay", "golf", "get satisfaction", "going", "Garden", "galaxy",
                            #H
                            "harris", "he", "heavy", "home", "HELP", "Hospital", "HOT", "HR", "henry", "high", "health care", "hunting", "hands", "hall",
                            "hollywood", "healthcare.com", "healthcare", "hosting.com", "hosting", "huge", "half", "hotels", 
                            #I
                            "inc", "internet", "ip", "it", "I", "I CAN", "Image", "Impact", "India", "Info", "Innovation", "Instant", "its", "internet alliance",
                            "inside", "it solutions", "internet marketing", "invoke", "idea", "ice", "ipo", "it management", "insurance.com", "insurance",
                            "irish", "ideas",
                            #J
                            "japan", "Johnson", "Joint", "Joy", "janet", "jennifer", "jobs", "jump", "juice", 
                            #K
                            "Kids", "king", "keep",
                            #L
                            "local", "Launch", "LIFE", "Light", "Living", "Location", "lopez", "llc", "law", "los", "libera", "links", "latino", "lunch", 
                            "like", "location labs", "lookout", "lawyers.com", "lawyer", "la.com", "la", "land", "less",  
                            #M
                            "media", "MADE", "Main", "Make", "MAN", "Mars", "Master", "MBA", "Me", "Meanwhile", "MEET", "More", "Mother", "Mr", "marc", "modern", 
                            "managing director", "modern", "miles", "massive", "minds", "maps", "match", "move", "motive", "music.com", "music", "mapping",                 "markets", "Marina", "managed", "movies", 
                            
                            #N
                            "networks", "network services", "new york post", "now", "National", "Native", "Nephew", "NEST", "Netbooks", "Nobel", "Noble", "Noise",
                            "news international", "new york media", "network solutions", "name", "Novel", "next",
                            #O
                            "one", "online", "open", "our", "outlook", "O", "Old National Bank", "One Result", "Orient", "Oversee", "online recruitment", "offers",
                            "oyster", "online publisher", "order", "others", "office live", "organic", "obvious", "opt", "outright",
                            #P
                            "press","protocol","pt", "P", "Partner", "Partners", "Patch", "Personal", "Pilot", "PLAY", "Plug", "Positive", "Powered",
                            "Pre", "Present", "President", "Private", "Pro", "Production", "Prototype", "Provide Support", "Public", "Pure", "pyramid",
                            "project", "pass", "payment processing", "people", "park", "promotions", "points", "power", "peel", "peek", "point of sale",
                            "prince", "plural", "patents", "perform group", "path", "phone", "parallel", "pc", "price.com", "price", "pc.com", "pc", "Point",
                            "pets", "pursuit",
                            #Q
                            "Quantum", 
                            #R
                            "rss", "Radio 2", "Reach", "Recruiting", "Release", "Resource", "reply", "respond", "research", "rentals", "results", "restaurant", 
                            "rainbow", "revolution", "registry", 
                            #S
                            "san", "search", "search engine", "seo", "school", "science", "she", "studios", "Salt", "SEA", "Secret", "SEE", "Share",
                            "Silk", "Simply Hired", "Six", "Skills", "Smile", "Smith", "Snow", "Solutions", "Southern", "Stage", "Start", "Start up",
                            "Startup", "State", "Style", "SUPPORT", "Systems", "self", "smart", "signs", "strategic", "sequence", "sweeps", "startups",
                            "source", "startup weekend", "s", "secure computing", "submit", "search technologies", "steam", "stanley", "simple", "smarter",
                            "sales", "student", "smart ads", "slots", "scout", "social media", "sanctuary", "sugar", "swap", "smart online", "several", 
                            "spectrum", "shine", "solve", "software.com", "software", "Shopping", "santa",
                            #T
                            "the network", "the orange", "they", "time", "tv", "Tablet", "TAKE", "TEA", "TEAM", "TEN", "Test", "The Game", "THE One",
                            "The Phone", "The Platform", "There", "THESE", "Thrive", "Tooling University", "Training", "technology partners", "ties",
                            "the cloud", "transfer", "true", "the planet", "turn", "trivia", "the street", "TED", "think", "trails", "them", "the next web", 
                            "talent", "tagged", "things", "total", "traffic", 
                            #U
                            "University", "Unnamed", "Upcoming", "Update", "users", "US Bank", "unleashed", "union", 
                            #V
                            "voice", "voip", "voip service", "V", "Via", "Vice", "Village", "vertical", "view", "virtualization", "vision", 
                            #W
                            "workshop", "Well", "Wellness", "West", "Where", "White", "Wind", "Wine", "web hosting design", "when", "webhosting", "wifi", "web", 
                            "wireless solutions", "weather", "way.com", "want",
                            #X
                            "x", 
                            #Y
                            "york",
                            #Z                 
                             ]
    user_defined_stopwords = ">|<".join(user_defined_stopwords).lower().split(">|<")
    overall_stopwords = nltk_stopwords + user_defined_stopwords
    return overall_stopwords
    


def get_website(test_string):
    #initialize the news_source
    website = ""
    #format url
    test_string = test_string.replace("http://", "")
    test_string = test_string.replace("www.", "")
    test_string = test_string.replace("/", " ")
    website = test_string.split()[0]
    #return the news_source
    return website
#----------------------------------------------------------------------------------------------
def load_pickle(filename):
    	#this function loads the pickle file
    	pkl_file = open(filename, 'rb')
    	dictionary = pickle.load(pkl_file)
    	pkl_file.close()
	return dictionary
#----------------------------------------------------------------------------------------------
def get_sent_from_paragraph(paragraph):
	#this function returns the individual sentences within the paragraph
	#splitting the paragraph based ".", "|", "?", "-"    	
	paragraph = paragraph.replace(".", "\t")
	paragraph = paragraph.replace("!", "\t")
	paragraph = paragraph.replace("?", "\t")
	paragraph = paragraph.replace(";", "\t")
	paragraph = paragraph.replace(",", "\t")
    	split_result = paragraph.split("\t")
	#splitting the split_result based on commas	
	total_result = []
	for each_result in split_result:
		comma_split_result = each_result.split(",")
		for each_split_result in comma_split_result:
			if each_split_result.find(" |") >= 0:
				index_split = each_split_result.find(" |")
				each_split_result = each_split_result[:index_split]
			if each_split_result.find(":") >= 0:
				index_split = each_split_result.find(":")
				each_split_result = each_split_result[index_split+1:]
			if each_split_result.find(" - ") >= 0:
				index_split = each_split_result.find(" - ")
				each_split_result = each_split_result[:index_split]
			each_split_result = each_split_result.replace("'s", "")
			each_split_result = get_space_removed(each_split_result)
			total_result.append(each_split_result)
			
	#return total_result	
	return total_result
#----------------------------------------------------------------------------------------------
def get_complete_tokens(each_sent):
    #this function returns every token in each_sent

    #determining uni_gram tokens
    unigram_tokens = nltk.word_tokenize(each_sent)

    #determine bi_gram tokens
    bi_gram = bigrams(unigram_tokens)
    bigram_tokens = []
    for tokens in bi_gram:
        bigram_tokens.append(' '.join(tokens))

    #determine tri_gram tokens
    tri_gram = trigrams(unigram_tokens)
    trigram_tokens = []
    for tokens in tri_gram:
            trigram_tokens.append(' '.join(tokens))       
    #determine complete list
    complete_token_list = []
    for token in unigram_tokens:
            complete_token_list.append(token.lower())
    for token in bigram_tokens:
            complete_token_list.append(token.lower())
    for token in trigram_tokens:
            complete_token_list.append(token.lower())
    return complete_token_list
#----------------------------------------------------------------------------------------------
def get_comp_name(complete_tokens, comp_id_dict):
	#this function returns the comp names after searching the complete tokens

	bad_comp_name_list = [
				#A
				"action","ad","artist", "awareness", "Automotive industry", "A", "A Company", "AB", "AC", "Active", "ADVANCED MEDIA",
				"Advanced Technology",	"AIR", "AL", "ALL", "Alumni", "Android", "Animal", "Ape", "APRIL", "As", "Assist", "Australia",
				"Author", "Awesome", "auditorium", "anthony", "alliance", "address", "app", "automotive", "applied system", "about", 
				"audience", "all media guide", "ambassador", "adaptive", "all covered", "ant", "act", "advertising.com", "advertising",
				"automatic", "access", "affinity", "Aerospace", 
				#B
				"blog", "buddy", "Ben", "BEST", "Between", "Blind", "BLUE", "Books", "Box", "Brain", "Bridge", "Broadcast", "Bus",
				"Business Consultants", "bank", "billy", "business solution", "bank", "bill", "better", "bundle", "beyond", "base",
				"become", "barcode", "blogs", "boom", "beach", "booking", "backstage", "business", "business.com", "business", "born.com", "born",
				"backcountry",
				#C
				"center", "ces", "chairman", "china", "C", "CA", "Cafe", "CAN", "Capital", "Card", "Challenge", "Cherry", "Chess", "CHOICE",
				"Club Website", "Co", "CODE", "College", "Company", "Connect", "CORE", "Create", "Cross", "CUT", "computer services", "closer", "cloud",
				"composite", "composite software", "content", "cast", "connected", "cable", "cars", "co-founder", "credit", "comedy", "candy",
				"collective", "current", "compass", "chill", "choose", "chat", "compute", "cloudy", "coastal.com", "coastal", "compete",
				"chicago.com", "chicago", "city", "city.com", "Care", "cfo", "case",
				#D
				"digital","digital media", "D", "December", "Design", "Desk", "Develop", "Director", "Directors", "Discovery", "Division",
				"Domain Registration", "Drive", "deliver", "data management", "data integration", "do", "data recovery", "daydream", "disco", 
				"ditto", "debt", "dns", "dec", "delivery", "delivery.com", "dog", "Dog.com", "diamond", "director of marketing", 
				#E
				"east", "edt", "enterprise", "Education", "Elements", "Energy", "Engage", "EU", "Exceptional", "Expand", "Explorer", "expression",
				"edge", "examiner" "elevate", "election", "entreprenuer", "expo", "expert", "Equities", "elastic" 
				#F
				"fabric", "far", "FACE", "Family", "FAST", "Fine", "Firm", "FIRST", "Five", "FORM", "Forty", "Foundation", "Franklin", "Free", 
				"Front", "Fuel", "fan", "fogs", "financial institution", "federal", "fitness", "founder", "force", "feedback", "focus",  
				"fry", "found", 
				#G
				"green", "group", "GAME", "Gate", "George", "Global", "Go", "GOOD", "guru", "grow", "get", "gmt", "good thing", "gifts", "giftcards",
				"genius", "gomez", "giving", "gameplay", "golf", "get satisfaction", "going", "Garden", "galaxy",
				#H
				"harris", "he", "heavy", "home", "HELP", "Hospital", "HOT", "HR", "henry", "high", "health care", "hunting", "hands", "hall",
				"hollywood", "healthcare.com", "healthcare", "hosting.com", "hosting", "huge", "half", "hotels", 
				#I
				"inc", "internet", "ip", "it", "I", "I CAN", "Image", "Impact", "India", "Info", "Innovation", "Instant", "its", "internet alliance",
				"inside", "it solutions", "internet marketing", "invoke", "idea", "ice", "ipo", "it management", "insurance.com", "insurance",
				"irish", "ideas",
				#J
				"japan", "Johnson", "Joint", "Joy", "janet", "jennifer", "jobs", "jump", "juice", 
				#K
				"Kids", "king", 
				#L
				"local", "Launch", "LIFE", "Light", "Living", "Location", "lopez", "llc", "law", "los", "libera", "links", "latino", "lunch", 
				"like", "location labs", "lookout", "lawyers.com", "lawyer", "la.com", "la", "land", "less",  
				#M
				"media", "MADE", "Main", "Make", "MAN", "Mars", "Master", "MBA", "Me", "Meanwhile", "MEET", "More", "Mother", "Mr", "marc", "modern", 
				"managing director", "modern", "miles", "massive", "minds", "maps", "match", "move", "motive", "music.com", "music", "mapping", 				"markets", "Marina", "managed", "movies", 
				
				#N
				"networks", "network services", "new york post", "now", "National", "Native", "Nephew", "NEST", "Netbooks", "Nobel", "Noble", "Noise",
				"news international", "new york media", "network solutions", "name", "Novel", "next",
				#O
				"one", "online", "open", "our", "outlook", "O", "Old National Bank", "One Result", "Orient", "Oversee", "online recruitment", "offers",
				"oyster", "online publisher", "order", "others", "office live", "organic", "obvious", "opt", "outright",
				#P
				"press","protocol","pt", "P", "Partner", "Partners", "Patch", "Personal", "Pilot", "PLAY", "Plug", "Positive", "Powered",
				"Pre", "Present", "President", "Private", "Pro", "Production", "Prototype", "Provide Support", "Public", "Pure", "pyramid",
				"project", "pass", "payment processing", "people", "park", "promotions", "points", "power", "peel", "peek", "point of sale",
				"prince", "plural", "patents", "perform group", "path", "phone", "parallel", "pc", "price.com", "price", "pc.com", "pc", "Point",
				"pets", "pursuit",
				
				#Q
				"Quantum", 
				#R
				"rss", "Radio 2", "Reach", "Recruiting", "Release", "Resource", "reply", "respond", "research", "rentals", "results", "restaurant", 
				"rainbow", "revolution", "registry", 
				#S
				"san", "search", "search engine", "seo", "school", "science", "she", "studios", "Salt", "SEA", "Secret", "SEE", "Share",
				"Silk", "Simply Hired", "Six", "Skills", "Smile", "Smith", "Snow", "Solutions", "Southern", "Stage", "Start", "Start up",
				"Startup", "State", "Style", "SUPPORT", "Systems", "self", "smart", "signs", "strategic", "sequence", "sweeps", "startups",
				"source", "startup weekend", "s", "secure computing", "submit", "search technologies", "steam", "stanley", "simple", "smarter",
				"sales", "student", "smart ads", "slots", "scout", "social media", "sanctuary", "sugar", "swap", "smart online", "several", 
				"spectrum", "shine", "solve", "software.com", "software", "Shopping", "santa",
				#T
				"the network", "the orange", "they", "time", "tv", "Tablet", "TAKE", "TEA", "TEAM", "TEN", "Test", "The Game", "THE One",
				"The Phone", "The Platform", "There", "THESE", "Thrive", "Tooling University", "Training", "technology partners", "ties",
				"the cloud", "transfer", "true", "the planet", "turn", "trivia", "the street", "TED", "think", "trails", "them", "the next web", 
				"talent", "tagged", "things", "total", "traffic", 
				#U
				"University", "Unnamed", "Upcoming", "Update", "users", "US Bank", "unleashed", "union", 
				#V
				"voice", "voip", "voip service", "V", "Via", "Vice", "Village", "vertical", "view", "virtualization", "vision", 
				#W
				"workshop", "Well", "Wellness", "West", "Where", "White", "Wind", "Wine", "web hosting design", "when", "webhosting", "wifi", "web", 
				"wireless solutions", "weather", "way.com",
				#X
				"x", 
				#Y
				"york",
				#Z				
		]
							
	#search for company names
	comp_name_list = []	
	bad_comp_name_list_lower = []

	for tokens in complete_tokens:
		if comp_id_dict.has_key(tokens.lower()):
			continue_trigger = True			
			for bad_comp_name in bad_comp_name_list:
				if tokens.lower() == bad_comp_name.lower():
					continue_trigger = False
					break
			if continue_trigger == True:
				comp_name_list.append(tokens.lower())

	#no duplicates
	comp_name_list = list(set(comp_name_list))	
	#remove small terms
	final_list = []
	for i, comp_name_i in enumerate(comp_name_list):
		overlap = False		
		for j, comp_name_j in enumerate(comp_name_list):
			if j != i:
				if comp_name_j.lower().find(comp_name_i.lower()) >= 0:
					if len(comp_name_j) > len(comp_name_i):
						final_list.append(comp_name_j)
					elif len(comp_name_i) > len(comp_name_j):
						final_list.append(comp_name_i)
					overlap = True
					break
		if overlap == False:
			final_list.append(comp_name_i)
	final_list = list(set(final_list))
	return final_list
#----------------------------------------------------------------------------------------------
def get_space_removed(sentence):
        #removes additional space at the front and back of the sentence
        #last updated 7/19/2012
	sentence = sentence.replace("and ", "")        
	if (len(sentence) == 1 and sentence == " ") or (len(sentence) == 0):
            sentence = "error" 
        continue_space_removal = True
        while continue_space_removal == True:
            if len(sentence) >= 1:
                if sentence[0] == " " or sentence[0] == "\t" or sentence[0] == "." or sentence[0] == "," or sentence[0] == ":" or sentence[0] == ";" or sentence[0] == "?":
                    sentence = sentence[1:]
                elif sentence[-1] == " " or sentence[-1] == "\t" or sentence[-1] == "." or sentence[-1] == "," or sentence[-1] == ":"  or sentence[-1] == ";" or sentence[-1] == "?":
                    sentence = sentence[:-1]
                else:
                    continue_space_removal = False 
            else:
                continue_space_removal = False
        return sentence
#----------------------------------------------------------------------------------------------
def get_date(date):
	#this function returns the date in "date" format
	split_date = date.split("-")
	return_date = []
	if len(split_date) > 0:	
		year = int(split_date[0])
		month = int(split_date[1])
		day = int(split_date[2].split(" ")[0])	
		return_date = [year, month, day]
	return return_date
#----------------------------------------------------------------------------------------------
#this function returns a file list from the news_source
def get_file_list(news_source):
	open_file = open(news_source, "r")
	file_list = open_file.readlines()
	open_file.close()
	return file_list
#----------------------------------------------------------------------------------------------
def get_processed_headline(headline):
	#this function returns the processed headline
	processed_headline = headline
	signs = ["|", ":", " - ", " -- ", "- ", " -"]
	for each_sign in signs:
                if processed_headline.find(each_sign) > 0:
                        if each_sign == ":":
                                processed_headline = processed_headline.split(each_sign)[1]
                        elif each_sign == " - ":
                                if len(processed_headline.split(each_sign)[0]) <= len(processed_headline.split(each_sign)[1]):
                                        processed_headline = processed_headline.split(each_sign)[1]
                                else:
                                        processed_headline = processed_headline.split(each_sign)[0]
                        else:
                               processed_headline = processed_headline.split(each_sign)[0] 
                        processed_headline = get_space_removed(processed_headline)
        return processed_headline
##	if headline.find("|") > 0:
##		processed_headline = headline.split("|")[0]
##		processed_headline = get_space_removed(processed_headline)
##	elif headline.find(":") > 0:
##		processed_headline = headline.split(":")[1]
##		processed_headline = get_space_removed(processed_headline)
##	elif headline.find(" - ") > 0:
##		processed_headline = headline.split(" - ")[1]
##		processed_headline = get_space_removed(processed_headline)
##	return processed_headline
#----------------------------------------------------------------------------------------------
#this function saves a pickle file
def save_pickle(dict_source, output_source):
    	output = open(output_source, 'wb')
    	pickle.dump(dict_source, output)
    	output.close()	
#---------------------------------------------------------------------------------------------------
#return a list, for example, ['us$115million']
#at around $75M-80M
#MySQL had generated more than $90 million in sales the year it was acquired
#by Sun Microsystems for $1 billion
#now the function can't distinguish examples like "$75M-$80M"
def get_money_area(sent):
        money_patterns = [
                                        "for .*([$] [0-9.-]+ [mb]\S*)",
                                        "for .*([$] [0-9.-]+[mb]\S*)",
                                        "for .*([$][0-9.-]+[mb]\S*)",
                                        "for .*([$][0-9.-]+ [mb]\S*)",

                                        "for .*(US[$] [0-9.-]+ [mb]\S*)",
                                        "for .*(US[$] [0-9.-]+[mb]\S*)",
                                        "for .*(US[$][0-9.-]+[mb]\S*)",
                                        "for .*(US[$][0-9.-]+ [mb]\S*)",
                                        ]
        for each_pattern in money_patterns:
                money_area = re.findall(each_pattern, sent, re.IGNORECASE)
                if len(money_area) > 0:
                        break

        return money_area
#---------------------------------------------------------------------------------------------------------
def get_minor_signs_removed(sentence):
        continue_space_removal = True
        while continue_space_removal == True:
            if len(sentence) >= 1:
                if sentence[0] == " " or sentence[0] == "\t" or sentence[0] == "." or sentence[0] == "," or sentence[0] == ":" or sentence[0] == ";" or sentence[0] == "?":
                    sentence = sentence[1:]
                elif sentence[-1] == " " or sentence[-1] == "\t" or sentence[-1] == "." or sentence[-1] == "," or sentence[-1] == ":"  or sentence[-1] == ";" or sentence[-1] == "?":
                    sentence = sentence[:-1]
                else:
                    continue_space_removal = False 
            else:
                continue_space_removal = False
        return sentence
#---------------------------------------------------------------------------------------------------------
def get_utf_8(string):
        processed_string = unicode(string, "ascii", "ignore")
        processed_string = processed_string.encode('utf8')
        return processed_string
#---------------------------------------------------------------------------------------------------------
def save_json(dict, filename):
	json.dump(dict, open(filename, "wb"))
#---------------------------------------------------------------------------------------------------------
def load_json(filename):
    #initialize dict
    dict = {}
	#defines dict
    open_file = open(filename, "r")
    dict = json.load(open_file)
    #return dict
    return dict
#---------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------
#fast way to find out the length of a large file
def get_file_length(file_name):
    with open(file_name) as temp_file:
        i = 0
        for i, j in enumerate(temp_file):
            pass
    if i == 0:
        return 0
    else:
        return i + 1
            


