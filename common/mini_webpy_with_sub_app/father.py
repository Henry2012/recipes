# -*- coding: utf-8 -*-

'''
Created on 2013-7-3

@author: Qiqun Han
'''


import web
import son

urls = (
        "/sub/", son.sub_app,
        '/', 'father',
        )

render = web.template.render('templates/')

class father:
    def GET(self):
        name = "QQ"
        
        return render.father(name)
    
if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
