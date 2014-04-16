#-*- coding:utf-8 -*-

'''
Created on 2013-7-30

@author: Qiqun.H
@classes: 
@methods: 
'''

from bottle import route, run, template

@route('/hello/<name>')
def index(name='world'):
    return template('hello {{name}}', name=name)

run(host='localhost', port=8080)