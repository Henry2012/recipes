# -*- coding: utf-8 -*-

'''
Created on Feb 25, 2013

@author: Qiqun Han
'''
#====================================================================
#====================================================================
#====================================================================
def timer(fn, *args, **kwargs):
    'Time the application of fn to args. Return (result, seconds).'
    import time
    start = time.clock()
    return fn(*args, **kwargs), time.clock() - start

class Timer():
    time = __import__('time')
    def __enter__(self):
        self.start = Timer.time.time()
        return self
    
    def __exit__(self, *args):
        self.end = Timer.time.time()
        self.interval = self.end - self.start
#====================================================================
#====================================================================
#====================================================================
class DisplayPkl():
    '''
    usage:
    d = DisplayPkl('../Auto_NLP/tier_1_latest_news.pkl')
    d.iterable_fmt()
    '''
    
    basic_functions = __import__('basic_functions')
    def __init__(self, pkl_filename):
        f = DisplayPkl.basic_functions.load_pickle(pkl_filename)
        self.f = f
        self.length = len(f)
        self.type = type(f)
        
    def dict_fmt(self, threshold):
        '''Pickle file contains only one dictionary.'''
        print 'The length of the file is %d' % self.length
        
        count = 0
        for key, value in self.f.iteritems():
            count += 1
            if count > threshold: break
            print key, value, type(key), type(value)
            print
#            if key == 'Cloudera': print 'C', value
#            if key == 'MapR': print 'M', value
            
    def list_fmt(self, threshold):
        '''Pickle file contains a list.'''
        from pprint import pprint
        print 'The length of the file is %d' % self.length
        
        for i, each in enumerate(self.f):
            if i > threshold: break
            pprint(each)
            
    def iterable_fmt(self, threshold=20):
        print 'The type of data in the file is %s' % self.type
        
        if isinstance(self.f, dict):
            self.dict_fmt(threshold)
        elif isinstance(self.f, (list, set)):
            self.list_fmt(threshold)
        else:
            print type(self.f)

#====================================================================
#====================================================================
#====================================================================
def sort_entities_upon_count(input_filename):
    '''
    Input:
        A    1
        B    4
        C    6
        ...
        
    Output:
        Sort based on the count
    '''
    with open(input_filename) as f:
        output = []
        for line in f:
            output.append(line.strip().split('\t'))

    output.sort(key=lambda x: int(x[1]), reverse=True)
    return output
#====================================================================       
#====================================================================
#====================================================================    
def save_as_txt(OneContainer, output_filename):
    '''
    Save a container with lists or tuples as its elements into a text file.
    '''
    with open(output_filename, 'w') as f:
        for each in OneContainer:
            f.write('\t'.join(each) + '\n')
#====================================================================    
#====================================================================
#====================================================================    
if __name__ == '__main__':
    
    if 0:
        print timer(sum, range(10000000))
        
    if 0:
        import httplib
        
        with Timer() as t:
            conn = httplib.HTTPConnection('baidu.com')
            conn.request('GET', '/')
        
        print('Request took %.03f sec.' % t.interval)
        
    if 1:
        
#        d = DisplayPkl('./test/company_id_name_2_5_2013.pkl')
#        d.iterable_fmt()
        
#        d2 = DisplayPkl('./test/everstring_corp_info_2_5_2013.pkl')
#        d2.iterable_fmt()

#        d3 = DisplayPkl('./test/related_comp_test_file.pkl')
#        d3.iterable_fmt()

#        d4 = DisplayPkl('./test/official_tags_12_06_2012.pkl')
#        d4.iterable_fmt()

#        d5 = DisplayPkl('./test/big_data_comp.pkl')
#        d5.iterable_fmt()
        
#        d6 = DisplayPkl('../CompName/related_comp/Cloudera_counters.pkl')
#        d6.iterable_fmt()
        
#        d7 = DisplayPkl('../fuzzy_matching/es_fund_raise_clustering_test_set_2_21_2013_ver1.pkl')
#        d7.iterable_fmt()

##        d8 = DisplayPkl('h:/han/eclipse/CompNameExpansion/competitors/rivals_in_nlp_ver2.pkl')
##        d8.iterable_fmt()

        # d9 = DisplayPkl('h:/han/eclipse/CompNameExpansion/competitors/specific_rivals_in_nlp_ver2.pkl')
        # d9.iterable_fmt()

#        d10 = DisplayPkl('H:/han/eclipse/CompNameExpansion/competitors/specific_rivals_in_crunchbase.pkl')
#        d10.iterable_fmt()

#        d11 = DisplayPkl('H:/han/eclipse/CompNameExpansion/competitors/domain2adwords.pkl')
#        d11.iterable_fmt()

#        d12 = DisplayPkl('H:/han/eclipse/CompNameExpansion/competitors/adword2domains.pkl')
#        d12.iterable_fmt()

##        d13 = DisplayPkl('H:/han/eclipse/CompNameExpansion/data_sources/filtered_tags_in_one_package_for_all_ver2.pkl')
##        d13.iterable_fmt()

		d14 = DisplayPkl('../auto_nlp_ver7/tier_1_2_latest_news_heading.pkl')
		d14.iterable_fmt()

    if 0:
        input_filename = r'E:\EverString\CaseStudies\Social TV\Viggle_updated.txt' 
        output_filename = r'E:\EverString\CaseStudies\Social TV\Viggle_updated_sorted.txt' 
        OneContainer = sort_entities_upon_count(input_filename)

        save_as_txt(OneContainer, output_filename)

    if 0:
        f = open(r'E:\EverString\CaseStudies\Social TV\Viggle_updated.txt')
        for each in f:
            print each
            raw_input()
