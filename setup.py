
#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import re, os
from qey import __version__
from qey import __author__
from qey import __email__

#commande
SCRIPTS = ['qey=qey.qey:main']

#requirements
def requirements():
    with open('requirements.txt','r',encoding = 'utf-8') as f:
        lines = f.readlines()
        return [line.replace('==','>=').strip() for line in lines]
REQUIREMENTS = requirements()

#readme
with open('README.md', 'r', encoding = 'utf-8') as f:
    README = '\n'.join(f.readlines())

#setup
setup(
    name='qey',
    version=__version__,
    description='Simple multiplatform hotstring script.',
    long_description_content_type='text/markdown',
    long_description=README,
    author=__author__,
    author_email=__email__,
    url='https://github.com/Whenti/qey',
    packages = ['qey'],
    package_dir={'qey':'qey'},
    package_data={'qey': ['qey/linux/*.py', 'qey/windows/*.exe']},
    include_package_data=True,
    install_requires=REQUIREMENTS,
    license='Apache License',
    zip_safe=False,
    keywords='multiplatform hotstring',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={
        'console_scripts': SCRIPTS,
    },
)
