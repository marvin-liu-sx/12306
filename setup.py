# -*- coding:utf-8 -*-

from codecs import open
from tickets import __version__
from setuptools import setup, find_packages

def read(f):
    return open(f, encoding='utf-8').read();



setup(
    name = 'tickets',
    version = __version__,
    description = 'Train tickets query via command line',
    packages = [ 'tickets' ],
    py_modules = ['run'],
    include_package_data = True,
    platforms = 'ubuntu14.04',
    install_requires = [
        'prettytable',
        'requests',
        'bs4'
        ],
    entry_point = {
        'console_scripts' : ['tickets=run:cli']
    },
    zip_false = False,
    classifiers = [
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: Cpython'
    ]
)

    
