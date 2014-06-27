#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: re.recipes.py
Description: this program deals with regex recipes.
Creation: 2013-11-6
Revision: 2013-11-6
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

import re
import pdb
from commonregex import CommonRegex

#===============================================================================
# Split string based on multiple delimiters
# 包含括号时，结果包含delimiters;不包含括号时，结果不包含delimiters
#===============================================================================
delimiters = "-|\|"  # delimiters = "[-|]"
assert re.split(delimiters, "1992-12-13") == ['1992', '12', '13']

assert re.split('\s+', 'a b c') == ['a', 'b', 'c']
assert re.split('\s+', 'a  b c') == ['a', 'b', 'c']
assert re.split('\s+?', 'a  b c') == ['a', '', 'b', 'c']

assert re.split('(\s+)', 'a b c') == ['a', ' ', 'b', ' ', 'c']
assert re.split('(\s+)', 'a  b c') == ['a', '  ', 'b', ' ', 'c']
assert re.split('(\s+?)', 'a  b c') == ['a', ' ', '', ' ', 'b', ' ', 'c']

# 以非[a-zA-Z0-9]的字符作为分隔符
print re.split('\W', 'pmc/ibm')
raw_input()

#===============================================================================
# re.match
#===============================================================================

#===============================================================================
# re.finditer
# 类似于re.findall,只不过返回的是封装好的类型，需要通过m.groups(1)来获得
# 而且m.groups(1)是tuple类型
#===============================================================================

#===============================================================================
# re.findall
# 通过括号返回欲抓取的字符串时，该方法直接返回字符串
#===============================================================================

#re.findall(pattern, string)

#===============================================================================
# re.search
#===============================================================================
text = """<td id="WWW_ADDRESS"><a href="http://www.spdb.com.cn">http://www.spdb.com.cn</a></td>"""
pattern = r"""<td id="WWW_ADDRESS"><a href="(.*)">"""

text = "泰达股份预计2011年净利降90%-100%"
pattern = r'([0-9]+%-[0-9]+%)'

print re.search(pattern, text)
match = re.search(pattern, text).group(1)
print match

#===============================================================================
# 正则表达式中含有中文
#===============================================================================

sent = "中石化大股东已增持"
pattern = r"增持.*股"
if re.search(pattern, sent):
    print "existing"
else:
    print "non-existing"
    
#===============================================================================
# 匹配ASCII
#     0. 首先将字符转换成Unicode
#     1. "[\x00-\x7F]"匹配ascii值为0-127的字符
#     2. "[\x00-\xFF]"匹配ascii值为0-255的字符
#===============================================================================

def contain_only_ascii(test, encoding='utf8'):
    test_in_unicode = test.decode(encoding)
    pattern = re.compile('[\x00-\x7F]', re.UNICODE)
    return all(re.match(pattern, each) for each in test_in_unicode)

#===============================================================================
# 匹配多个字符串：要求至少有一个存在
# str1|str2|str3
#     1. r'aa|b'  匹配'aa'或者'b'
#     2. r'a{?:a|b}'  匹配'aa'或者'ab'
#===============================================================================

sent = "[conj(指出-5, 华意压缩-1), conj(盈利-5, 份额-3), cc(盈利-5, 与-4), nsubj(提升-7, 盈利-5),"
pattern = r'conj\(盈利|指出(\-)[0-9]+, .+-[0-9]+\)'

# another test case
sent = "b"
pattern = r'aa|b'

groups = re.search(re.compile(pattern), sent)
if groups:
    print "yes!!!"
else:
    print "No"

#===============================================================================
# 后向断言 & 后向否定断言
#     1. (?=...)
#     2. (?!...)
#===============================================================================

sent = 'QIqunHan is a great man'
pattern = r'(?<!Q[iI]qun)Han'
m = re.search(pattern, sent)
if m:
    print 'Found', m.groups()
else:
    print "Not found"
raw_input()
    
#===============================================================================
# 匹配特殊字符，所有标点符号（包含空格）
#===============================================================================

print '---beginning---'
print u'\u2018'
print u'\u2019'
print u'\u201a'
print u'\u201b'
print [unicode('a', 'utf8')]
print [unicode('，', 'utf8')]
print [unicode(',', 'utf8')]
print [u'万']
print [u'元']
print '---ending---'

sent = "我是中国人"

# 匹配英文字符之外的字符
if re.search(r'\W', sent):
    for each in re.findall(ur'([\u4e00-\u9fa5]+)', unicode(sent, 'utf8')):
        print each

#===============================================================================
# 匹配数值
#===============================================================================

pattern = ur'[0-9\.]+-+[0-9\.]+'
sent = u'云海金属一季度净利预亏680-920万'
sent = u'南都电源预计上半年净利增1.8-2.1倍'

pattern = ur'[0-9\.]+.{0,1}-+[0-9\.]+.{0,1}'
pattern = ur'[0-9\.]+.{0,2}-+[0-9\.]+.{0,2}'
sent = u'振东制药2011年净利润预增30%--50%'
sent = u'永安林业预计去年亏损4500万-6000万'
# sent = u'安科生物净利润预增17.35%-25.05%'
sent = u'环旭电子发行价区间7.5元---8元'
sent = u'东北证券1-6月净利润大增149.91%'
sent = u'华泰证券-美的电器-000527-战略转型显成效,整体上市开启新纪元'

# print re.search(pattern, sent).group()

#===============================================================================
# 使用github上的包CommonRegex
#===============================================================================

sent = u'[长江证券]长江证券晨会纪要08-5-26'
sent = u'中信证券晨会-0731'
parse = CommonRegex(sent)
print parse.dates

#===============================================================================
# 用regex进行字符串替换
# pattern = "<\s*link\s+.*href\s*=\s*(.*?)\s+.*?>"
# Java: <\\s*[lL][Ii][nN][kK]\\s+.*[hH][Rr][eE][fF]\\s*=\\s*(.*?)\\s+.*?>
#===============================================================================

pattern = r'(<\s*[lL][Ii][nN][kK]\s+.*[hH][Rr][eE][fF]\s*=\s*).*?(\s+.*?>)'
s = '''<link HREF= "css/public.CSS?v=2014004081807.css"  type="text/css" rel="stylesheet" >kjhkjhkhjkhjkhty
< link href ='css/public.css?v=2014004081807.css'  type="text/css" rel="stylesheet" >'''
print re.sub(pattern, r"\1'Qiqun'\2", s)

pattern = r'<\s*[lL][Ii][nN][kK]\s+.*[hH][Rr][eE][fF]\s*=\s*(.*?)\s+.*?>'
s = '''<link HREF= "css/public.CSS?v=2014004081807.css"  type="text/css" rel="stylesheet" >kjhkjhkhjkhjkhty
< link href ='css/public.css?v=2014004081807.css'  type="text/css" rel="stylesheet" >asdfa
< link href ='css/public.css?v=2014004081807.css'  type="text/css" rel="stylesheet" >'''
print re.findall(pattern, s)
raw_input()

if __name__ == "__main__":
    test = '中国'
    
    test_in_unicode = test.decode('utf8')
    print contain_only_ascii(test)