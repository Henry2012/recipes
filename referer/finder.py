#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: referer.finder.py
Creation: 2013-12-31
Revision: 2013-12-31
"""

import os
import json

from query_introducer import queries

try:
    from urlparse import urlparse, parse_qsl
    iteritems = lambda dikt: dikt.iteritems()
    text_type = unicode
except ImportError:  # urlparse was renamed urllib.parse in Python 3
    from urllib.parse import urlparse, parse_qsl
    iteritems = lambda dikt: dikt.items()
    text_type = str

def load_referers(json_file):
    referers_dict = {}
    with open(json_file) as json_content:
        for medium, conf_list in iteritems(json.load(json_content)):
            for referer_name, config in iteritems(conf_list):
                params = None
                if 'parameters' in config:
                    params = list(map(text_type.lower, config['parameters']))
                for domain in config['domains']:
                    referers_dict[domain] = {
                        'name': referer_name,
                        'medium': medium
                    }
                    if params is not None:
                        referers_dict[domain]['params'] = params
    return referers_dict

# JSON_FILE = os.path.join(os.path.dirname(__file__), 'data', 'referers.json')
JSON_FILE = os.path.join(os.path.dirname(__file__), "..", "io", 'referers_in_china.json')
REFERERS = load_referers(JSON_FILE)

class Referer(object):
    def __init__(self, ref_url, curr_url=None, referers=REFERERS):
        self.known = False
        self.referer = None
        self.medium = 'unknown'
        self.search_parameter = None
        self.search_term = None
        self.referers = referers

        ref_uri = urlparse(ref_url)
        ref_host = ref_uri.hostname
        self.known = ref_uri.scheme in {'http', 'https'}
        self.uri = ref_uri

        if not self.known:
            return

        if curr_url:
            curr_uri = urlparse(curr_url)
            curr_host = curr_uri.hostname
            if curr_host == ref_host:
                self.medium = 'internal'
                return

        referer = self._lookup_referer(ref_host, ref_uri.path, True)
        if not referer:
            referer = self._lookup_referer(ref_host, ref_uri.path, False)
            if not referer:
                self.medium = 'unknown'
                return

        self.referer = referer['name']
        self.medium = referer['medium']
        
        if referer['medium'] == 'search':
            if 'params' not in referer or not referer['params']:
                return
            for param, val in parse_qsl(ref_uri.query):
                if param.lower() in referer['params']:
                    self.search_parameter = param
                    self.search_term = val

    def _lookup_referer(self, ref_host, ref_path, include_path):
        referer = None
        try:
            if include_path:
                referer = self.referers[ref_host + ref_path]
            else:
                referer = self.referers[ref_host]
        except KeyError:
            if include_path:
                path_parts = ref_path.split('/')
                if len(path_parts) > 1:
                    try:
                        referer = self.referers[ref_host + '/' + path_parts[1]]
                    except KeyError:
                        pass
        if not referer:
            try:
                idx = ref_host.index('.')
                return self._lookup_referer(
                    ref_host[idx + 1:],
                    ref_path, include_path
                )
            except ValueError:
                return None
        else:
            return referer

def get_search_term(url):
    r = Referer(url)
    term = r.search_term
    
    if not term:
        parsed = urlparse(url)
        for (key, value) in parse_qsl(parsed.query):
            if key in queries:
                term = value
                break
    return term

if __name__ == "__main__":
    urls = ["http://wenwen.soso.com/z/Search.e?sp=Spython&w=python&search=%E6%90%9C%E7%B4%A2%E7%AD%94%E6%A1%88",
            "http://news.sogou.com/news?p=70330301&query=amazon",
            "http://www.sogou.com/web?query=python&p=&w=03021800",
            "http://www.sogou.com/web?ie=utf8&query=python&_ast=1388391936&_asf=null&w=01029901&sut=2496&sst0=1388392032242&lkt=6%2C1388392031306%2C1388392032055",
            "http://baike.so.com/search?ie=utf-8&q=python&src=tab_wenda",
            "https://www.google.com.hk/search?hl=zh-CN&gl=cn&tbm=nws&authuser=0&q=likeqiang&oq=likeqiang&gs_l=news-cc.3..43j43i53.1748.2138.0.3292.9.2.0.3.0.1.219.329.0j1j1.2.0...0.0...1ac.1.1nd5i673_AI",
            "http://sou.autohome.com.cn/zonghe?q=%d1%a9%b7%f0%c0%bc&entry=1",
            "http://search.xgo.com.cn/all.php?keyword=%B0%C2%B5%CF&tijiao=+",
            "http://beijing.taoche.com/chevrolet/?sw=python",
            "http://www.youdao.com/search?q=python&ue=utf8&keyfrom=web.index",
            "http://news.youdao.com/search?q=python&keyfrom=web.top"]

    for url in urls:
        print get_search_term(url)