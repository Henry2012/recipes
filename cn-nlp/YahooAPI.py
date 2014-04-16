#-*- coding:utf-8 -*-

"""
#Name: Yi Jin
#Company: EverString
#File: YahooAPI_SectorExpansion_ver1.py
#Description: this program contains functions for yahoo searches  
#$Revision: 5/18/2013$
"""

#===============================================================================
# import library reference
#===============================================================================
import httplib2, json, oauth2, time, urllib
from datetime import datetime
from pprint import pprint

#===============================================================================
# global class
#===============================================================================
class YahooAPI(object):

    def __init__(self):
        self.consumer_key = "dj0yJmk9OTlOOXhGbzFZalJIJmQ9WVdrOVpHRm5TMXBYTm1zbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD0zMA--"
        self.consumer_secret = "fe35739c5083f386b0c3abbf24e59934195736ca"
        
    def getYahooEncodedQuery(self, combo):
        formatted_query = ['"' + x + '"' for x in combo]
        query = " ".join(formatted_query)
        query = query.replace("\u00a3", "�").replace("\u20ac","�")
        #print query
        query = urllib.urlencode({"q" : query})
        query = query.replace("+", "%20").replace('"', "%22")
        return query
    
    def getOauthHeader(self, url):
        consumer = oauth2.Consumer(key=self.consumer_key,secret=self.consumer_secret)
        params = {
            'oauth_version': '1.0',
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': int(time.time()),
        }
        
        oauth_request = oauth2.Request(method='GET', url=url, parameters=params)
        oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, None)
        oauth_header=oauth_request.to_header(realm='yahooapis.com')
        return oauth_header
    
    #this function returns the batch results from the YahooAPI search
    #Input:    type: the type of search, it could be "web" or "news"
    #          query: the query term
    #          start_count: starting count, by default it starts at 1
    #          count: maximum number of results, by default it is set to 50, the maximum result is 1000
    def getResults(self, type, query, start_count, count):
        results_list = []
        pages = int(count/50)+1
        query = urllib.urlencode({"q" :query}).replace("+", "%20")
        for i in range(0, pages):
            if type == "web":
                url = "http://yboss.yahooapis.com/ysearch/"+type+"?" + query + "&abstract=long&count="+str(50)+"&start="+str(0+i*50)
            elif type == "news":
                url = "http://yboss.yahooapis.com/ysearch/"+type+"?" + query + "&count="+str(50)+"&start="+str(0+i*50)                
            oauth_header = self.getOauthHeader(url)
            # Get search results
            http = httplib2.Http()
            resp, content = http.request(url, 'GET', headers=oauth_header)
            try:
                results = json.loads(content)
            except:
                results = {}
            if results:
                results_list += self.getProcessedResults(type, results)
        return results_list
    
    def getProcessedResults(self, type, results):
        results_list = []
        if results:
            if type in results["bossresponse"]:
                if "results" in results["bossresponse"][type]:
                    for res in results["bossresponse"][type]["results"]:
                        results_list.append(res)
        return results_list
    
    def getQueryCount(self, type, query):
        #===============================================================================
        # 1. type could be 'web' or 'news'
        # 2. query可以使用引号，用来全字匹配
        #===============================================================================
        query_count = None
        query = urllib.urlencode({"q" :query}).replace("+", "%20")
        if type == "web":
            url = "http://yboss.yahooapis.com/ysearch/"+type+"?" + query + "&abstract=long&count=1&start=1"
        elif type == "news":
            url = "http://yboss.yahooapis.com/ysearch/"+type+"?" + query + "&count=1&start=1"                
        oauth_header = self.getOauthHeader(url)
        # Get search results
        http = httplib2.Http()
        resp, content = http.request(url, 'GET', headers=oauth_header)
        try:
            results = json.loads(content)
        except:
            results = {}
        if results:
            if type in results["bossresponse"]:
                if "totalresults" in results["bossresponse"][type]:
                    query_count = results["bossresponse"][type]["totalresults"]
        return query_count

if __name__ == "__main__":
    import pdb
    from timer import Timer
    es_yahoo_api = YahooAPI()
    
    #===============================================================================
    # 返回结果有keys:
    # [u'dispurl', u'title', u'url', u'abstract', u'clickurl', u'date']
    #===============================================================================
    with Timer() as t_:
        with open('io/acqu.txt') as acq:
            with open('io/acqu_trainset_v2.txt', 'w') as acq_train:
                count_of_titles = 0
                count_of_events_with_search_results = 0 
                for i, line in enumerate(acq):
                    if not (i % 10):
                        print '[ INFO ] # lines: ', i
                    line = line.strip()
                    if line:
                        companies = company_1, company_2 = tuple(line.split('\t'))
                        query = '"%s" "%s" site:cs.com.cn' % companies
                        with Timer() as t:
                            search_results = es_yahoo_api.getResults("web", query, 1, 1000)
                        #print '[ INFO ] time consumed: ', t.interval
                        if search_results:
                            count_of_events_with_search_results += 1
                            for result in search_results:
                                title = result.get('title', None)
                                url = result.get('url', None)
#                                 dispurl = result.get('url', None)
#                                 clickurl = result.get('clickurl', None)
#                                 pdb.set_trace()
                                if (company_1 in title or
                                    company_2 in title) and url:
                                    count_of_titles += 1
                                    new_line = '%s\t%s\t%s\t%s\n' % (title, company_1, company_2, url)
                                    acq_train.write(new_line)
                            
                print '[ INFO ] # titles: ', count_of_titles
                print '[ INFO ] # events_with_search_results: ', count_of_events_with_search_results
        print '[ INFO ] time consumed for all: ', t_
    
    #===============================================================================
    # 获得搜索关键字的搜索数量
    #===============================================================================            
#     query_count = es_yahoo_api.getQueryCount("web", "'wearable technology'")
#     print query_count
