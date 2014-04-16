#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: egg_builder.setup.py
Description: this program
Creation: 2013-12-5
Revision: 2013-12-5
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys

setup_requires = []

if 'test' in sys.argv:
    setup_requires.append('pytest')

setup(
    name='hello_world',
    version='0.1.0',
    author='Qiqun.H',
    description=(
        'Hello World'
    ),
    long_description=open('README.rst').read(),
    py_modules=['hello_world'],
)

#===============================================================================
# Simple Version
#===============================================================================

from distutils.core import setup
 
 
setup(name='chronic',
      version='0.3.2',
      py_modules=['chronic', 'proxy'],
      packages=['signals'],
      description='Half profiler, half timer, 100% fun.',
      url='http://github.com/davidcrawford/chronic',
      author='David Crawford',
      author_email='david.crawford@gmail.com',
      license='MIT'
      )