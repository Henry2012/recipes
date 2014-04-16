#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han
Company: EverString Technology Ltd.
File: egg_builder.setup.py
Creation: 2013-12-5
Revision: 2013-12-5
Copyright (c) All Right Reserved, EverString Technology Ltd., http://www.everstring.com
"""

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys

setup_requires = []

if 'test' in sys.argv:
    setup_requires.append('pytest')

setup(
    name='referer',
    version='0.1.0',
    author='Qiqun.H',
    description=(
        'referer---extracting marketing attribution data (such as search terms)'
    ),
    long_description=open('README.rst').read(),
    packages = find_packages(),
)
