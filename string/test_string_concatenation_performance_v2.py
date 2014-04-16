
from cStringIO import StringIO
import time, commands, os
from sys import argv
from pprint import pprint

def method1():
    out_str = ''
    for num in xrange(loop_count):
        out_str += `num`
    ps_stats()
    return out_str

def method2():
    from UserString import MutableString
    out_str = MutableString()
    for num in xrange(loop_count):
        out_str += `num`
    ps_stats()
    return out_str

def method3():
    from array import array
    char_array = array('c')
    for num in xrange(loop_count):
        char_array.fromstring(`num`)
    ps_stats()
    return char_array.tostring()

def method4():
    str_list = []
    for num in xrange(loop_count):
        str_list.append(`num`)
    out_str = ''.join(str_list)
    ps_stats()
    return out_str

def method5():
    file_str = StringIO()
    for num in xrange(loop_count):
        file_str.write(`num`)
    out_str = file_str.getvalue()
    ps_stats()
    return out_str

def method6():
    out_str = ''.join([`num` for num in xrange(loop_count)])
    ps_stats()
    return out_str


def ps_stats():
    global process_size
    ps = commands.getoutput('ps -up ' + `pid`)

    process_size = ps.split()[15]
    

def call_method(num):
    global process_size
    start = time.time()
    z = eval('method' + str(num))()
    elapsed = time.time() - start
    print "method", num
    print "time", elapsed
    print "output size ", len(z) / 1024, "kb"
    print "process size", process_size, "kb"
    print
    
loop_count = 100000
pid = os.getpid()

if len(argv) == 2:
    call_method(argv[1])
else:
    print "Usage: python stest.py <n>\n" \
        "  where n is the method number to test"
