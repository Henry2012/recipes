# -*- coding: utf-8 -*-

'''
Created on 2013-7-16

@author: Qiqun Han
'''

import web
import external_handler_class

urls = (
        "/hello/", "OneUrlHandler",
        "/", "Index",
        )

render = web.template.render('templates/')

class Index:
    def GET(self):
        name = "QQ"
        
        return render.index(name)


if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()