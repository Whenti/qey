
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

QEY_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),'qey')

#commande
COMMANDE = ['{c}=qey.{c}:main'.format(c=command) for command in COMMANDS]

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
    name='pyqo',
    version=__version__,
    description='Useful collection of command line scripts.',
    long_description_content_type='text/markdown',
    long_description=README,
    author=__author__,
    author_email=__email__,
    url='https://github.com/Whenti/pyqo',
    packages = ['pyqo'],
    package_data={'pyqo': ['data/*.json']},
    package_dir={'pyqo':'pyqo'},
    include_package_data=True,
    install_requires=REQUIREMENTS,
    license='Apache License',
    zip_safe=False,
    keywords='pip requirements imports',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    scripts = SCRIPTS,
    entry_points={
        'console_scripts': CONSOLE_SCRIPTS,
    },
)
>>>>>>> oupsi
