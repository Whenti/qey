#! /usr/bin/env python3
"""
    The ``._json`` module
    ======================
    Contains all the functions related to the reading and mofifications of the ``.json`` files
"""

import json
import os
import sys

def read_json(filename):
    if os.path.isfile(filename):
        with open(filename, encoding='utf-8') as f:
            data = json.loads(f.read())
    else:
        data = {}
    return data

def get_json(filename, keys):
    data = read_json(filename)
    l = []
    for key in keys:
        if key in data:
            l.append(data[key])
        else:
            print('The key "{}" has no attributed value.'.format(key))
            del key
    return l

def write_json(filename, data):
    with open(filename, 'w', encoding = 'utf-8') as f:
        json.dump(data, f)

def set_json(filename, map):
    data = read_json(filename)
    for key, value in map.items():
        data[key] = value
    write_json(filename, data)

def remove_json(filename, keys):
    data = read_json(filename)
    for key in keys:
        data.pop(key)
    write_json(filename, data)
