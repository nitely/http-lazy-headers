#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

BASE_DIR = os.path.join(os.path.dirname(__file__))

with open(os.path.join(BASE_DIR, 'requirements.txt')) as f:
    REQUIREMENTS = f.read()

URL = 'https://github.com/nitely/http-lazy-headers'
README = """
HLH is an abstraction over raw HTTP headers, providing:

* Lazy decoding, parsing and validation of input headers
* Eager validation and lazy formatting of output headers
* Methods and helpers for common operations
* A headers collection on top of `OrderedDict` for fast lookups
* WSGI support
* A pure Python implementation without using regex!
* A sane API
* A way out of messy strings manipulation and typos

Specs support: rfc7230, rfc7231, rfc7232, rfc7233, rfc7234, rfc7235
rfc6265, rfc3986, rfc5646, rfc6266, rfc1034, rfc5234
"""
VERSION = __import__('http_lazy_headers').__version__


setup(
    name='http-lazy-headers',
    version=VERSION,
    description='Parse, validate and format HTTP headers lazily',
    author='Esteban Castro Borsani',
    author_email='ecastroborsani@gmail.com',
    long_description=README,
    url=URL,
    packages=find_packages(exclude=['tests']),
    test_suite="runtests.start",
    zip_safe=False,
    include_package_data=True,
    install_requires=REQUIREMENTS,
    setup_requires=REQUIREMENTS,
    license='MIT License',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'])
