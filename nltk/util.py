#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: nltk.util.py
Description: this program comes from nltk.util
Creation: 2014-2-10
Revision: 2014-2-10
"""
import textwrap

def tokenwrap(tokens, separator=" ", width=70):
    """
    Pretty print a list of text tokens, breaking lines on whitespace

    :param tokens: the tokens to print
    :type tokens: list
    :param separator: the string to use to separate tokens
    :type separator: str
    :param width: the display width (default=70)
    :type width: int
    """
    return '\n'.join(textwrap.wrap(separator.join(tokens), width=width))

if __name__ == "__main__":
    tks = [str(i) for i in range(1000)]
    print tokenwrap(tks)