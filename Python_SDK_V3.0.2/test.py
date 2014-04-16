#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
#=============================================================================
#
#     FileName: test.py
#         Desc:
#
#       Author: dantezhu
#
#      Created: 2011-10-19 10:23:23
#      Version: 3.0.0
#      History:
#               3.0.0 | dantezhu | 2011-10-19 10:23:23 | initialization
#
#=============================================================================
'''
import json

from openapi_v3 import OpenAPIV3

appid = 600
appkey = '04017120b52c43cbb6b1c7d87fd042c9'
#appid = 22792
#appkey = '783bd021f6934265aaadf2c17e82e8e6'
#appid = 18218 
#appkey = '2a59aa1b618645d88d14d5c10a3b0064'
#appid = 611
#appkey = '17d5950636664c6b9e783ac5672759b3'
#appid = 613
#appkey = 'd2703adccaa143a983a62a62830ccf97'
#appid = 100615705
#appkey = 'ac973999547d83b46072fc4178e4c35c'
#appid = 32585
#appkey = '73bfa85035ff45e28d68a5c335f93e6a'
#appid = 22804
#appkey = 'dcf7e22ad0f5471f80de748fab3d9543'
#appid = 28433
#appkey = '97ba9099139a4493a8486f15eb41d545'
#appid = 100623064
#appkey = '303358c80f79472081056688f0e84d07'
#appid = 200253080
#appkey = 'OgK0SfPKVf256YTG'
#appid = 100645379
#appkey = 'f5bc5f2f31ba5f5a579dd16aa952ac70'

iplist = ('172.27.0.91',)
#iplist = ('10.6.207.119:9191',)
#iplist = ('10.166.146.171',)
#iplist = ('10.166.146.174',)
#iplist = ('172.25.36.57:8191',)
#iplist = ('proxy.qq.com',)

#openid = ''
#openkey = ''
openid = '0000000000000000000000000039811C'
openkey = 'BAA4A7F86ABCE56A4FC98AD0B81FB542'
#openid = '21429811590D8B5BE6981E037344324D'
#openkey = '9814423FCE2CF220A45D3A9E5D994DFC'
#openid = '00000000000000000000000000A72202'
#openkey = '25CA869BCBBCC0208BA994E70D44EF26'
#openid = '0000000000000000000000000039811C'
#openkey = 'A76BFD10E5C5753F385958E0CEC5A640'
#openid = '000000000000000100000000076A9AF6'
#openkey = '4B6F4AFEAA82A32B150D94E4AE867D731DFED5B5D5A8992C'
#openid = '00000000000000000000000005BA61AE'
#openkey = 'F0F8BE248AA94CE38CC3F7F35E5E3FD1'
#openid = 'A65190D83B534D931FA6F9A445442855'
#openkey = '43D0CF01790D795D6415C55B2AF2EF22'
#openid = '00000000000000000000000000A72202'
#openkey = 'A602A6A897CEC2D7B29F044861903F87'
#openid = '00000000000000000000000005AB758B'
#openkey = 'D5A934D87C45E764FB71D84BEC4D4C84'


api = OpenAPIV3(appid, appkey, iplist)

def pretty_show(jdata):
    import json
    print json.dumps(jdata, indent=4, ensure_ascii=False).encode('utf8')

def qz_core_test():
    pf = 'qzone'

    jdata = api.call('/v3/user/get_info', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey
    })
    pretty_show(jdata)

    jdata = api.call('/v3/relation/get_app_friends', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey
    })
    pretty_show(jdata)

    openidlist = []
    if jdata['ret'] == 0:
      openidlist = [fid['openid'] for fid in jdata['items']]

    jdata = api.call('/v3/user/get_multi_info', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey,
        'fopenids': '_'.join(openidlist)
    })
    pretty_show(jdata)

    jdata = api.call('/v3/user/is_setup', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey
    })
    pretty_show(jdata)

    jdata = api.call('/v3/relation/is_friend', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey,
        'fopenid': '0000000000000000000000000326E4AA'
    })
    pretty_show(jdata)

    jdata = api.call('/v3/user/get_rich_info', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey
    })
    pretty_show(jdata)

    jdata = api.call('/v3/relation/get_all_friends', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey
    })
    pretty_show(jdata)

def qp_core_test():
    pf = 'qplus'

    jdata = api.call('/v3/user/get_info', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey
    })
    pretty_show(jdata)

    jdata = api.call('/v3/relation/get_app_friends', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey
    })
    pretty_show(jdata)

    openidlist = []
    if jdata['ret'] == 0:
      openidlist = [fid['openid'] for fid in jdata['items']]

    jdata = api.call('/v3/user/get_multi_info', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey,
        'fopenids': '_'.join(openidlist)
    })
    pretty_show(jdata)

    jdata = api.call('/v3/user/is_setup', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey
    })
    pretty_show(jdata)

    jdata = api.call('/v3/relation/is_friend', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey,
        'fopenid': '0000000000000000000000000326E4AA'
    })
    pretty_show(jdata)

    jdata = api.call('/v3/user/get_rich_info', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey
    })
    pretty_show(jdata)

    jdata = api.call('/v3/relation/get_all_friends', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey
    })
    pretty_show(jdata)

def py_core_test():
    pf = 'pengyou'

    jdata = api.call('/v3/user/get_info', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey
    })
    pretty_show(jdata)

    jdata = api.call('/v3/relation/get_app_friends', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey
    })
    pretty_show(jdata)

    openidlist = []
    if jdata['ret'] == 0:
       openidlist = [fid['openid'] for fid in jdata['items']]

    jdata = api.call('/v3/user/get_multi_info', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey,
        'fopenids': '_'.join(openidlist)
    })
    pretty_show(jdata)

    jdata = api.call('/v3/user/is_setup', {
       'pf': pf,
       'openid': openid,
       'openkey': openkey
    })
    pretty_show(jdata)

    jdata = api.call('/v3/relation/is_friend', {
       'pf': pf,
       'openid': openid,
       'openkey': openkey,
       'fopenid': '0000000000000000000000000326E4AA'
    })
    pretty_show(jdata)

    jdata = api.call('/v3/user/get_rich_info', {
      'pf': pf,
      'openid': openid,
      'openkey': openkey
    })
    pretty_show(jdata)

    jdata = api.call('/v3/relation/get_all_friends', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey
    })
    pretty_show(jdata)

def kx_core_test():
    pf = 'kapp'

    jdata = api.call('/v3/user/get_info', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey
    })
    pretty_show(jdata)

    jdata = api.call('/v3/relation/get_app_friends', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey
    })
    pretty_show(jdata)

    openidlist = []
    if jdata['ret'] == 0:
       openidlist = [fid['openid'] for fid in jdata['items']]

    jdata = api.call('/v3/user/get_multi_info', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey,
        'fopenids': '_'.join(openidlist)
    })
    pretty_show(jdata)

    jdata = api.call('/v3/user/is_setup', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey
    })
    pretty_show(jdata)

    jdata = api.call('/v3/relation/is_friend', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey,
        'fopenid': '00000000000000010000000005881504'
    })
    pretty_show(jdata)

def manyou_core_test():
    pf = 'manyou100'

    jdata = api.call('/v3/user/get_info', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey
    })
    pretty_show(jdata)

    jdata = api.call('/v3/relation/get_app_friends', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey
    })
    pretty_show(jdata)

    openidlist = []
    if jdata['ret'] == 0:
       openidlist = [fid['openid'] for fid in jdata['items']]

    jdata = api.call('/v3/user/get_multi_info', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey,
        'fopenids': '_'.join(openidlist)
    })
    pretty_show(jdata)

    jdata = api.call('/v3/user/is_setup', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey
    })
    pretty_show(jdata)

    jdata = api.call('/v3/relation/is_friend', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey,
        'fopenid': '00000000000000000000000007B673FF'
    })
    pretty_show(jdata)

def xingcloud_core_test():
    pf = 'xingcloud'

    jdata = api.call('/v3/user/is_login_xingcloud', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey
    })
    pretty_show(jdata)

    jdata = api.call('/v3/user/get_info', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey
    })
    pretty_show(jdata)

    jdata = api.call('/v3/relation/get_app_friends', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey
    })
    pretty_show(jdata)

    openidlist = []
    if jdata['ret'] == 0:
       openidlist = [fid['openid'] for fid in jdata['items']]

    jdata = api.call('/v3/user/get_multi_info', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey,
        'fopenids': '_'.join(openidlist)
    })
    pretty_show(jdata)

    jdata = api.call('/v3/user/is_setup', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey
    })
    pretty_show(jdata)

    jdata = api.call('/v3/relation/is_friend', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey,
        'fopenid': '0000000000000000000000000326E4AA'
    })
    pretty_show(jdata)

def t_core_test():
    pf = 'tapp'
    jdata = api.call('/v3/user/get_info', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey
    })
    pretty_show(jdata)

    jdata = api.call('/v3/relation/get_app_friends', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey
    })
    pretty_show(jdata)

    openidlist = []
    if jdata['ret'] == 0:
       openidlist = [fid['openid'] for fid in jdata['items']]

    jdata = api.call('/v3/user/get_multi_info', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey,
        'fopenids': '_'.join(openidlist)
    })
    pretty_show(jdata)

def t_other_test():
    pf = 'tapp'

    #jdata = api.call('/v3/relation/add_idol', {
        #'pf': pf,
        #'openid': openid,
        #'openkey': openkey,
        #'fopenids': '00000000000000000000000001223930',
    #})
    #pretty_show(jdata)

    jdata = api.call('/v3/user/get_other_info', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey,
        'fopenid': openid,
    })
    pretty_show(jdata)

def qqshow_test():
    pf = 'qzone'

    jdata = api.call('/v3/qqshow/get_app_friends', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey,
        'cmd': 0
    })
    pretty_show(jdata)
    

def iedstar_test():
    pf = 'qzone'

    jdata = api.call('/v3/user/is_area_login', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey,
    })
    pretty_show(jdata)
    
def unity_test():
    pf = 'qzone'

    jdata = api.call('/v3/user/set_achivement', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey,
        'user_attr': json.dumps(dict(level=10), ensure_ascii=False),
    })
    pretty_show(jdata)

    jdata = api.call('/v3/user/get_achivement', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey,
        'fopenids': '0000000000000000000000000326E4AA_0000000000000000000000000039811C',
    })
    pretty_show(jdata)
    return

    jdata = api.call('/v3/user/friends_vip_info', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey,
        'fopenids': '0000000000000000000000000326E4AA_0000000000000000000000000039811C',
    })
    pretty_show(jdata)

    jdata = api.call('/v3/user/is_vip', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey,
    })
    pretty_show(jdata)

    jdata = api.call('/v3/user/is_login', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey,
    })
    pretty_show(jdata)

    jdata = api.call('/v3/spread/verify_invkey', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey,
        'iopenid': '0000000000000000000000000039811C',
        'itime': '1334202931',
        'invkey': '8A96E97D5F393241F04CFD0255550241'
    })
    pretty_show(jdata)

def csec_test():
    pf = 'qzone'

    jdata = api.call('/v3/csec/word_filter', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey,
        'content': '唉'*1000,
    })
    pretty_show(jdata)

    jdata = api.call('/v3/csec/is_forbidden', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey,
    })
    pretty_show(jdata)



def music_test():
    pf = 'qzone'

    jdata = api.call('/v3/music/get_song_info', {
        'pf': pf,
        'openid': openid,
        'openkey': openkey,
    })
    pretty_show(jdata)

def main():
    #qz_core_test()
    #qp_core_test()
    #py_core_test()
    #kx_core_test()
    #manyou_core_test()
    #xingcloud_core_test()
    #t_core_test()
    #t_other_test()
    #qqshow_test()
    #iedstar_test()
    #unity_test()
    #csec_test()
    music_test()

if __name__ == '__main__':
    for it in range(0, 1000):
        if it == 1:
            break
        main()
