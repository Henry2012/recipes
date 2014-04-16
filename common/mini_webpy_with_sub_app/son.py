# -*- coding: utf-8 -*-

'''
Created on 2013-7-3

@author: Qiqun Han
'''

import web

urls = ('hello/(.*)', 'son')

render = web.template.render('templates/')

class son:
    def GET(self, name):
        
        return render.son(name)
    
sub_app = web.application(urls, locals())

