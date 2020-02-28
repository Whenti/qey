#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from qey import __version__
from qey import __author__
from qey import __email__

# command
SCRIPTS = ['qey=qey.qey:main']

# readme
with open('README.md', 'r', encoding = 'utf-8') as f:
    README = '\n'.join(f.readlines())

# setup
setup(
    name='qey',
    version=__version__,
    description='Simple multi-platform hotstring handler.',
    long_description_content_type='text/markdown',
    long_description=README,
    author=__author__,
    author_email=__email__,
    url='https://github.com/Whenti/qey',
    packages=['qey'],
    package_dir={'qey': 'qey'},
    include_package_data=True,
    license='Apache License',
    zip_safe=False,
    keywords='multi-platform hotstring',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={
        'console_scripts': SCRIPTS,
    }, install_requires=['psutil']
)
