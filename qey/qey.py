#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
## Command ``qey``
"""

import click
from .start import start
from .setstartup import setstartup

@click.command()
@click.argument('arg')
def main(arg):
    """qey principal command."""
    if arg=='startup':


if __name__ == "__main__":
    main()
