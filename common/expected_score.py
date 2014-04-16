# -*- coding: utf-8 -*-

'''
Created on 2013-5-7

@author: QQ.Han
@module: 
'''

import math

def get_factor(rating):
    
    return math.pow(10, rating/400.0)

def get_elo_rating(rating_a, rating_b):
    "Elo rating system"
    
    factor_a = get_factor(rating_a)
    factor_b = get_factor(rating_b)
    
    return factor_a/(factor_a + factor_b)

if __name__ == "__main__":
    
     print get_elo_rating(1613, 1609)
     print get_elo_rating(1613, 1477)