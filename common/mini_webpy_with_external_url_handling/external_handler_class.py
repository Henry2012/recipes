# -*- coding: utf-8 -*-

'''
Created on 2013-7-16

@author: Qiqun Han
'''

import web

render = web.template.render('templates/')

class OneUrlHandler:
    def GET(self):
        name = "Qiqun"
        
        return render.index(name)