# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os
import fnmatch

requires = [
    "tornado==4.0",
    "tornado-redis==2.4.17",
]

setup(
    name='lexr.us',
    version='0.1.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=['app'],
    include_package_data=True,
    install_requires=requires,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'lexr.us = app:main',
        ]
    },
    data_files=[
        ('public', ['src/public/index.html']),
        ('public/scripts', ['src/public/scripts/main.js']),
        ('public/styles', ['src/public/styles/main.css']),
    ]
)
