#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
## Command ``qey``
"""

import click
import os
from .utils import *
from .start import start, stop
from .setstartup import setstartup

@click.command()
@click.argument('arg', nargs=1)
def main(arg):
    """qey principal command."""

    if not os.path.isdir(CONFIG_PATH):
        os.mkdir(CONFIG_PATH)
    if not os.path.isdir(CONFIG_QEY_PATH):
        os.mkdir(CONFIG_QEY_PATH)
    if not os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE,'w',encoding='utf-8') as f:
            f.write('{"PATHS" : []}')

    if arg=='startup':
        setstartup()
    elif arg=='start':
        start()
    elif arg=='stop':
        stop()

if __name__ == "__main__":
    main()
