# -*- coding: utf-8 -*-

'''
Created on 2013-8-20

@author: Qiqun.H

Reference
1. urllib2: http://docs.python.org/2/howto/urllib2.html
'''

import urllib2
#from bs4 import BeautifulSoup
from lxml import etree
#from pprint import pprint
#from StringIO import StringIO

url = "http://www.agilent.com/about/newsroom/presrel/?cat=all&start=1&page=1"
response = urllib2.urlopen(url)
html_page = response.read()

#soup = BeautifulSoup(page)

#f = StringIO(soup)
#f = StringIO('''<table><tr><td>2013-08-19</td></tr></table>''')

#-------------------------------
'''
Raise an Exception: lxml.etree.XMLSyntaxError,
because here html_page is a HTML5 document,
rather than a XML doc.

So we should use html.fromstring(),
rather than etree.fromstring(html_page)
'''
#f = html.fromstring(html_page)

#Still raise an exception:
#TypeError: cannot parse from 'HtmlElement'
#tree = html.parse(f)
#-------------------------------

tree = etree.HTML(html_page)
print tree.xpath('/table')
# print len(tree.xpath("table"))

# for tr in tree.xpath("//table/tbody/tr"):
#     print dir(tr)
#     raw_input()
#     print tr.text





# r = tree.xpath('//table/tr')
# print len(r)

# doc = html.fromstring(soup)
# print etree.tostring(doc)
