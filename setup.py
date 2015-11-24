#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup file for the SkCode project.
"""

import os
from setuptools import setup

import skcode


# Dump readme content as text
with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# Setup config
setup(
    name='skcode',
    version=skcode.__version__,
    author='Fabien Batteix',
    author_email='fabien.batteix@tamialab.fr',
    packages=['skcode', 'skcode.tags', 'skcode.utility'],
    include_package_data=True,
    license='GPLv3',
    description='SkCode - BBcode parser implementation for Python 3.4',
    long_description=README,
    url='https://github.com/TamiaLab/PySkCode',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Topic :: Text Processing :: Markup',
        'Topic :: Text Processing :: Markup :: HTML',
    ],
    install_requires=['pygments'],
    tests_require=['nose', 'coverage'],
)
