# -*- coding: utf-8 -*-

'''
Created on 2013-5-23

@author: QQ.Han
'''

from ConfigParser import SafeConfigParser
parser = SafeConfigParser()

if 1:
    
    parser.read("../io/test.txt")
    
    print parser.get('bug_tracker', 'pwd')
    print parser.get('bug_tracker', 'pwd_v1')
    print [parser.get('bug_tracker', 'pwd_v2')]
    print parser.items('bug_tracker')
    print '-' * 50
    print parser.get('bug', 'pwd')
    print parser.items('bug')

raw_input()

#####################################################
''' 
read() method also accepts a list of filenames.
Each name in turn is scanned, and if the file exists it is opened and read.
'''

if 0:
    candidates = ['does_not_exist.ini', 'also_does_not_exist.ini',
                  'simple.ini']
    found = parser.read(candidates)
    missing = set(candidates) - set(found)
    
    print "found:    ", sorted(found)
    print "missing:  ", sorted(missing)
    
#####################################################
'''
The module below fails to work.

UnicodeDecodeError: 'utf8' codec can't decode byte 0xa8 in position 2: invalid start byte
'''

if 0:
    import codecs
#     print "CP1"
    with codecs.open('unicode.ini', 'r', encoding='utf-8') as f:
        parser.readfp(f)
#     print 'CP2'   
    pwd = parser.get('bug_tracker', 'pwd')
    print 'Password:', pwd.encode('utf-8')
    print 'Type:', type(pwd)
    print 'repr():', repr(pwd)
    
#####################################################

'''
Traverse the config file

- Access all sections, corresponding options and items

sections() returns a list of strings
options(section_name) returns a list of strings
items(section_name) returns a list of tuples containing the name-value pairs
'''
    
if 0:
     
    parser.read('multisection.ini')
    
    for section in parser.sections():
        print "Section: ", section
        
        options = parser.options(section)
        print "Options: ", options
        
        items = parser.items(section)
        for name, value in items:
            print "    %s = %s" % (name, value)
        
#####################################################

'''
use has_section() & has_option() method beforehand to
avoid exceptions when using get()
'''
            
#####################################################

'''
getfloat()
getint()
getboolean()
'''

if 0:
     
    parser.read('types.ini')
    
    items = parser.items('ints')
    print items
    
    for option in parser.options('ints'):
        print type(parser.getint('ints', option))
        print type(parser.get('ints', option))
        
    for option in parser.options('floats'):
        print parser.getfloat('floats', option)
        print parser.get('floats', option)
        
    for option in parser.options('booleans'):
        print parser.getboolean('booleans', option)
        print parser.get('booleans', option)

#####################################################

'''
using interpolation & DEFAULT, like variables in Environment variable

[bug_tracker]
protocol = http
server = localhost
port = 8080
url = %(protocol)s://%(server)s:%(port)s/bugs/

parser.get('bug_tracker', 'url') --> 'http://localhost:8080/bugs/'
'''

if 1:
    parser.read('interpolation_defaults.ini')
    print parser.get('bug_tracker', 'url')