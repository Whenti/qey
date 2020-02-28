#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The ``json_handling`` module
======================
Contains all the functions related to the reading and modifications of the ``.json`` files.
"""

import json
import os

from typing import Dict, Any


def read_json(filename: str):
    if os.path.isfile(filename):
        with open(filename, encoding='utf-8') as f:
            data = json.loads(f.read())
    else:
        data = {}
    return data


def write_json(filename: str, data: Dict[str, Any]):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f)
