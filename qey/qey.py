#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
## Command ``qey``
"""

import click
import os
from .utils import *
from .start import start as _start
from .start import stop as _stop
from .setstartup import setstartup as _setstartup
from .json import *

if not os.path.isdir(CONFIG_PATH):
    os.mkdir(CONFIG_PATH)
if not os.path.isdir(CONFIG_QEY_PATH):
    os.mkdir(CONFIG_QEY_PATH)
if not os.path.isfile(CONFIG_FILE):
    with open(CONFIG_FILE,'w',encoding='utf-8') as f:
        f.write('{"INI_FILE" : ""}')
if not os.path.isdir(PIDS_PATH):
    os.mkdir(PIDS_PATH)

@click.group()
@click.pass_context
def main(ctx):
    pass

@main.command()
def start():
    """Start `qey`."""
    _start()

@main.command()
def stop():
    """Stop `qey`."""
    _stop()

@main.command()
@click.option('--set/--unset', default=True)
def startup(set):
    """Make `qey` start on startup."""
    _setstartup(set)

@main.command()
@click.argument('filename', type=click.Path(exists=True), required=True)
def setfile(filename):
    """Set the INI file containing hotstrings."""
    set_json(CONFIG_FILE, {"INI_FILE" : os.path.abspath(filename)})

if __name__ == "__main__":
    main()
