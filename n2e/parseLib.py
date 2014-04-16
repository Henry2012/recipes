#-*- coding:utf-8 -*-

"""
#Name: Yi Jin
#Date: 6/24/2013
#Company: EverString
#File: parseLib.py
#Description: this class returns a parseLib
"""

def get_dependency_dict():
    dep_num_type = {
                        "0": "abbrev",
                        "1": "acomp",
                        "2": "advcl",
                        "3": "advmod",
                        "4": "agent",
                        "5": "amod",
                        "6": "appos",
                        "7": "attr",
                        "8": "aux",
                        "9": "auxpass",
                        "10": "cc",
                        "11": "ccomp",
                        "12": "complm",
                        "13": "conj",
                        "14": "cop",
                        "15": "csubj",
                        "16": "csubjpass",
                        "17": "dep",
                        "18": "det",
                        "19": "dobj",
                        "20": "expl",
                        "21": "infmod",
                        "22": "iobj",
                        "23": "mark",
                        "24": "mwe",
                        "25": "neg",
                        "26": "nn",
                        "27": "npadvmod",
                        "28": "nsubj",
                        "29": "nsubjpass",
                        "30": "num",
                        "31": "number",
                        "32": "parataxis",
                        "33": "partmod",
                        "34": "pcomp",
                        "35": "pobj",
                        "36": "poss",
                        "37": "possessive",
                        "38": "preconj",
                        "39": "predet",
                        "40": "prep",
                        "41": "prepc",
                        "42": "prt",
                        "43": "punct",
                        "44": "purpcl",
                        "45": "quantmod",
                        "46": "rcmod",
                        "47": "ref",
                        "48": "rel",
                        "49": "root",
                        "50": "tmod",
                        "51": "xcomp",
                        "52": "xsubj",
                        "53": "prep_on",
                        "54": "prep_in",
                        }
    dep_type_num = {}
    for each_num in dep_num_type:
        dep_type_num[dep_num_type[each_num]] = each_num
    return [dep_num_type, dep_type_num]
    


 