#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: codec.recipes.py
Description: this program deals with coder-decoder.
Creation: 2013-11-7
Revision: 2013-11-7
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""
import pdb
import re

#===============================================================================
# 配置文件的value是中文的话，需要以UTF-8无BOM格式
#===============================================================================
#===============================================================================
# Set default encoding
# 有如下一个问题：
#     1. Windows环境下将Unicode写入txt文本，不存在UnicodeEncodeError
#     2. Ubuntu环境下利用相同的程序写文本，却存在问题
#     3. 解决方案：首先将Unicode显式地转换成UTF-8或者在程序前加上如下的setdefaultencoding
#===============================================================================

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

#===============================================================================
# 1.Get the integer value of the char
# 2.Convert back
# 3.Get a Unicode object of an integer
#===============================================================================

assert ord('a') == 97
assert chr(97) == 'a'
assert unichr(97) == u'a'

#===============================================================================
# Type checking using type() or isinstance() functions
#===============================================================================
assert type(unichr(97)) == unicode
assert isinstance(unichr(97), unicode) == True
assert isinstance(chr(97), str) == True

#===============================================================================
# ignore errors
#===============================================================================
'line'.encode('utf-8', errors='ignore')

#===============================================================================
# Force all string to be utf8
# Borrowed from: http://www.codigomanso.com/en/2010/05/una-de-python-force_unicode/
#===============================================================================

def force_unicode(s, encoding='utf-8', errors='ignore'):
    """
    Returns a unicode object representing s. Treats bytestrings using the
    'encoding' codec.
    """
    if s is None:
        return u''
    try:
        if not isinstance(s, basestring,):
            if hasattr(s, '__unicode__'):
                s = unicode(s)
            else:
                try:
                    s = unicode(str(s), encoding, errors)
                except UnicodeEncodeError:
                    if not isinstance(s, Exception):
                        raise
                    # If we get to here, the caller has passed in an Exception
                    # subclass populated with non-ASCII data without special
                    # handling to display as a string. We need to handle this
                    # without raising a further exception. We do an
                    # approximation to what the Exception's standard str()
                    # output should be.
                    s = ' '.join(force_unicode(arg, encoding, errors) for arg in s)
        elif not isinstance(s, unicode):
            # Note: We use .decode() here, instead of unicode(s, encoding,
            # errors), so that if s is a SafeString, it ends up being a
            # SafeUnicode at the end.
            s = s.decode(encoding, errors)
    except UnicodeDecodeError as e:
        if not isinstance(s, Exception):
            raise UnicodeDecodeError(s, *e.args)
        else:
            # If we get to here, the caller has passed in an Exception
            # subclass populated with non-ASCII bytestring data without a
            # working unicode method. Try to handle this without raising a
            # further exception by individually forcing the exception args
            # to unicode.
            s = ' '.join(force_unicode(arg, encoding, errors) for arg in s)
    return unicode(s)

#===============================================================================
# 只匹配ASCII为0-127的字符
#===============================================================================

def contain_only_ascii(test, encoding='utf8'):
    test_in_unicode = test.decode(encoding)
    pattern = re.compile('[\x00-\x7F]', re.UNICODE)
    return all(re.match(pattern, each) for each in test_in_unicode)

#===============================================================================
# 查看中文标点符号的unicode
#===============================================================================

for each in [u'：', u'。', u'‘', u'“']:
    print [each]

print 'beginning'
print u'\u2018'
print u'\u2019'
print u'\u201a'
print u'\u201b'
print 'ending'

print '\xd3\xc5\xbb\xdd\x84\xbb\xb3\xd5\xba\xba\xa1\xaa\xa1\xaa\xc2\xed\xcc\xd8 \xb0\xee\xc4\xc9'.decode('GB2312')
raw_input()

if __name__ == "__main__":
    
#     s = "ヘルプ"
#     assert force_unicode(s) == "ヘルプ"
#     assert type(force_unicode(s)) == unicode

#     s1 = ['D:\\PythonStuff\\LogAnalysisFromZhifeng\\io\\txt\\000281_0', '171072', 'http://www.baidu.com/s?wd=%D3%F0%C3%AB%C7%F2++%C0%AD%CF%DF%B0%F5%CA%FD&tn=sogouie_dg', '\xd3\xf0\xc3\xab\xc7\xf2++\xc0\xad\xcf\xdf\xb0\xf5\xca\xfd', u'\u7fbd\u6bdb\u7403>|<++>|<\u62c9\u7ebf>|<\u78c5\u6570']
#     with open("../io/_test.txt", 'w') as wf:
#         s1[-2] = s1[-2].decode("gbk")
#         wf.write("\t".join(s1))
    
    for each in ["ヘルプ",
                 "möchten",
                 "gehört"]:
        print unicode(each)

    #===============================================================================
    # 要求在打开文件时就将UTF8转换成Unicode
    # 这样就能够实现：
#         1. len("光大证券") == 12 | len(u"光大证券") == 4
#         2. 字符串匹配时，可以用unicode也可以不用unicode
#         3. 求出index时需要unicode
    #===============================================================================

#     import codecs
#     
#     with codecs.open('../io/test.txt', 'r', 'utf-8') as f:
#         for each in f:
#             print each.split('\t')
#             print u"光大证券" in each
#             print ""
#             print each.index(u'光大证券')
#             print len(u'光大证券')
#             print len('光大证券')
#             
#     with codecs.open('../io/test.txt', 'a', 'utf-8') as af:
#         af.write(u'广大')
