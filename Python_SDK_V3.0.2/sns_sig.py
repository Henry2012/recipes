#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
#=============================================================================
#
#     FileName: sns_sig.py
#         Desc: 生成签名
#
#       Author: open.qq.com
#
#      Created: 2011-09-07 16:58:12
#      Version: 3.0.0
#      History:
#               3.0.0 | dantezhu | 2011-09-07 16:58:12 | initialization
#
#=============================================================================
'''
import urllib
import binascii
import hashlib
import hmac

def mk_soucrce(method, url_path, params):
    str_params = urllib.quote("&".join(k + "=" + str(params[k]) for k in sorted(params.keys())), '')

    source = '%s&%s&%s' % (
        method.upper(),
        urllib.quote(url_path,''),
        str_params
    )

    return source
    

def hmac_sha1_sig(method, url_path, params, secret):
    source = mk_soucrce(method, url_path, params)
    hashed = hmac.new(secret, source, hashlib.sha1)
    return binascii.b2a_base64(hashed.digest())[:-1]


def main():
    method = 'GET'
    url_path = '/cgi-bin/video/video_insert'
    params = {
        'provider_id': 1,
        'src_id': 100,
        'name': '我爱你'
    }

    secret = '9b7adbd2ee5206224135&'

    print mk_soucrce(method, url_path, params)
    print hmac_sha1_sig(method, url_path, params, secret)

if __name__ == '__main__':
    main()
