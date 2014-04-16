#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: cookie.recipe.py
Description: this program
Creation: 2014-4-8
Revision: 2014-4-8
"""

import Cookie
import urllib

c = Cookie.SimpleCookie()
c.load('bdshare_firstime=1364119634072; lzstat_uv=642728970699726231|2322437; CNZZDATA30031420=cnzz_eid%3D820957983-1364119772-http%253A%252F%252Fwww.qire123.com%26ntime%3D1380422168%26cnzz_a%3D1%26ltime%3D1380422167423%26rtime%3D68; pp_vod_v=%u7075%u4E66%u5999%u63A2%u7B2C%u516D%u5B63%7C%u7B2C1%u96C6^http%3A//www.qire123.com/videos/58224vod-play-id-58224-sid-0-pid-0.html_$_%u8BC6%u9AA8%u5BFB%u8E2A%u7B2C%u4E5D%u5B63%7C%u7B2C2%u96C6^http%3A//www.qire123.com/videos/59378vod-play-id-59378-sid-0-pid-1.html_$_%u751F%u6D3B%u5927%u7206%u70B8%u7B2C%u4E03%u5B63%7C%u7B2C2%u96C6^http%3A//www.qire123.com/videos/56528vod-play-id-56528-sid-0-pid-1.html_$_%u6D77%u519B%u7F6A%u6848%u8C03%u67E5%u5904%u7B2C%u5341%u4E00%u5B63%7C%u7B2C01%u96C6^http%3A//www.qire123.com/videos/59069vod-play-id-59069-sid-0-pid-0.html_$_%u597D%u6C49%u4E24%u4E2A%u534A%u7B2C%u5341%u4E00%u5B63%7C%u7B2C1%u96C6^http%3A//www.qire123.com/videos/59556vod-play-id-59556-s')

for key, morsel in c.iteritems():
    print morsel.key
    print morsel.value
    print urllib.unquote(morsel.value)
    print
