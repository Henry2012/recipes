#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author: Qiqun Han
File: rabbitmq.recipes.py
Description: this program
Creation: 2013-11-25
Revision: 2013-11-25
"""

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost', port=8080))

channel = connection.channel()