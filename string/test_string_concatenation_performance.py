def timer(fn, *args, **kwargs):
    'Time the application of fn to args. Return (result, seconds).'
    import time
    start = time.clock()
    return fn(*args, **kwargs), time.clock() - start

def method1(count):
    out = ""
    for i in xrange(count):
        out += str(i)
        
    return out

def method2(count):
    out = ""
    for i in xrange(count):
        out += `i`
        
    return out

def method3(count):
    return ''.join(`i` for i in xrange(count))

def method4(count):
    return ''.join([`i` for i in xrange(count)])

def method5(count):
    return ''.join(`i` for i in range(count))

def method6(count):
    return ''.join([`i` for i in range(count)])

if __name__ == "__main__":
    '''
    Results in order:
    0.00646802370984
    0.0039128403308
    0.00209156112136
    0.00175222908595
    0.00213200476512
    0.00195839302607
    
    Conclusion:
    1. xrange确实比range运行时间短，可也没有多大体现
    2. list comprehension里使用圆括号，而不是方括号，运行时间反而更长'''
    
    print timer(method1, 1000)[1]
    print timer(method2, 1000)[1]
    
    print timer(method3, 1000)[1]
    print timer(method4, 1000)[1]
    print timer(method5, 1000)[1]
    print timer(method6, 1000)[1]