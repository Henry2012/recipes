#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: iterators_and_alike.rock_paper_scissors.py
Description: this program
Creation: 2014-3-7
Revision: 2014-3-7
"""

import pdb

def advance_generator_once(original_fn):
    def actuall_call(*args, **kw):
        gen = original_fn(*args, **kw)
        assert gen.next() is None
        return gen
    return actuall_call

@advance_generator_once
def rock_paper_scissors():
    valid = 'rps'
    wins = 'rs', 'pr', 'sp'
    result = None
    
    while 1:
        chosen = [None, None]
        while None in chosen:
            player, play = yield result
            result = None
            if play in valid:
                chosen[player] = play
            else:
                print 'invalid input'
        
        if chosen[0] + chosen[1] in wins:
            result = ('win', 0) + tuple(chosen)
        elif chosen[1] + chosen[0] in wins:
            result = ('win', 1) + tuple(chosen)
        else:
            result = ('tie', None) + tuple(chosen)

if __name__ == "__main__":
    
    rps = rock_paper_scissors()
    pdb.set_trace()