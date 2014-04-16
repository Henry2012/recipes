import sys
# try:
#     raise Exception("a")
# except:
#     try:
#         raise Exception("b")
#     except:
#         raise
    

# try:
#     {'a': 1}[5]
#     1, 0
# except Exception, e:
#     #e = sys.exc_info()[0]
#     #print e
#     
#     # (5,)
#     print e.args
#      
#     #print str(e)

d = (1, 2)

try:
    a, b, c = d
except Exception, e:
    '''
    <type 'tuple'>
    ('need more than 2 values to unpack',)'''
    print type(e.args)
    print e.args
    
    '''
    <type 'tuple'>
    (<type 'exceptions.ValueError'>, 
     ValueError('need more than 2 values to unpack',), 
     <traceback object at 0x020D3F30>)'''
    print type(sys.exc_info())
    print sys.exc_info()
    
    e.args += (d,)
    raise

