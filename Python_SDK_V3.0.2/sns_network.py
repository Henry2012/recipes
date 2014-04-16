#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
#=============================================================================
#
#     FileName: sns_network.py
#         Desc: 开放平台的http协议发送包
#
#       Author: open.qq.com
#
#      Created: 2011-03-03 14:52:04
#      Version: 3.0.0
#      History:
#               3.0.0 | dantezhu | 2011-03-03 14:52:04 | initialization
#
#=============================================================================
'''

import socket
import copy
import urllib,urllib2
from random import choice
import httplib

try:
    import json
except ImportError:
    import simplejson as json


from sns_sig import hmac_sha1_sig

class SNSNetwork(object):
    _iplist = ['172.27.0.91',]
    _secret = ''
    _sig_name = 'sig'

    def __init__(self, secret, iplist=None, sig_name=None):
        '''
        iplist:         ip列表，也可以传入域名
        '''
        self._secret = secret
        if iplist:
            self._iplist = copy.deepcopy(iplist)

        if sig_name:
            self._sig_name = sig_name

    def _mk_send_data(self, method, url_path, params):
        '''
        返回datapair:ec_params
        '''
        sig = hmac_sha1_sig(method, url_path, params, self._secret)
        params[self._sig_name] = sig

        ec_params = urllib.urlencode(params)

        return ec_params


    def _http_send(self, method, url_path, ec_params):
        '''
        提供一个统一的调用API接口
        '''

        uri = 'http://%s%s' % (choice(self._iplist), url_path)

        if method.lower() == 'post':
            data = urllib2.urlopen(uri,ec_params).read()
        elif method.lower() == 'get':
            if ec_params:
                dest_url = '%s?%s' % (uri, ec_params)
            else:
                dest_url = uri
            data = urllib2.urlopen(dest_url).read()
        else:
            raise TypeError, 'method invalid:%s' % method

        return data

    def _https_send(self, method, url_path, ec_params):
        conn = httplib.HTTPSConnection(choice(self._iplist))

        method = method.upper()

        if method == 'GET':
            url = '%s?%s' % (url_path, ec_params)
            conn.request(method, url)
        else:
            conn.request(method, url_path, ec_params)

        rsp = conn.getresponse()

        if rsp.status != 200:
            raise ValueError, 'status:%d' % rsp.status
        data = rsp.read()

        return data


    def open(self, method, url_path, params, protocol='http'):
        '''
        对外提供使用
        '''

        ec_params = self._mk_send_data(method, url_path, copy.deepcopy(params))

        if protocol == 'http':
            data = self._http_send(method, url_path, ec_params)
        elif protocol == 'https':
            data = self._https_send(method, url_path, ec_params)
        else:
            raise TypeError,'protocol invalid:%s' % protocol

        return data


def main():
    api = SNSNetwork('wokao&')
    print api.open('get', '/user/info', {'openid':1, 'openkey':2})

if __name__ == '__main__':
    socket.setdefaulttimeout(5)
    main()
