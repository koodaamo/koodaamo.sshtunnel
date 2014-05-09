#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='koodaamo.sshtunnel',
    version='0.1.0',
    description='SSH Tunneling library based on Twisted',
    long_description=readme + '\n\n' + history,
    author='Petri Savolainen',
    author_email='petri.savolainen@koodaamo.fi',
    url='https://github.com/petri/koodaamo.sshtunnel',
    namespace_packages=['koodaamo'],
    packages = ['koodaamo.sshtunnel'],
    include_package_data=True,
    install_requires=[
        "twisted",
        "pyCrypto",
        "docopt",
        "setuptools",
    ],
    entry_points="""
       [console_scripts]
       tunnel = koodaamo.sshtunnel.sshtunnel:tunnel
    """,
    license="BSD",
    zip_safe=False,
    keywords='koodaamo.sshtunnel',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests.test_suite',
)