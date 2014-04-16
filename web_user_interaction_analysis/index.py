# -*- coding: utf-8 -*-

'''
Created on 2013-7-31

@author: Qiqun.H
'''

import data
import web
import re
import base64

urls = (
        '/login', 'Login',
        '/', 'Index',
        )

app = web.application(urls, globals())
render = web.template.render('templates/')

allowed = (('es', 'webtracking'),
           ('qq', 'fibonacci'))

class Index:
    def GET(self):
        if web.ctx.env.get('HTTP_AUTHORIZATION') is not None:
            web_analytics = data.WebUserInteractionAnalytics()
            user_login_info = web_analytics.get_last_login_datetime()
            return render.index(user_login_info)
        else:
            raise web.seeother('/login')

class Login:
    def GET(self):
        auth = web.ctx.env.get('HTTP_AUTHORIZATION')
        authreq = False
        if auth is None:
            authreq = True
        else:
            auth = re.sub('^Basic ', '', auth)
            username, password = base64.decodestring(auth).split(':')
            if (username, password) in allowed:
                raise web.seeother('/')
            else:
                authreq = True
        if authreq:
            web.header('WWW-Authenticate', 'Basic realm="Auth"')
            web.ctx.status = '401 Unauthorized'
            return

class User:
    def GET(self):
        user = web.input().u
        web_analytics = data.WebUserInteractionAnalytics()
        all_info_for_one_user = web_analytics.get_all_info_for_one_user(user)
        return render.user(all_info_for_one_user)

if __name__ == '__main__':
    
    app.run()
