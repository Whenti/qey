#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
## Command ``qey``
"""
import argparse
import os
import sys
import subprocess
import psutil
from qey.json_handling import read_json, write_json
from qey.hotkeys_handling import write_hotstrings, get_hotstrings
from qey.os_detection import is_linux

WELCOME_MESSAGE = """
Welcome to the wonderful world of                          
  __ _  ___ _   _ 
 / _` |/ _ \ | | |
| (_| |  __/ |_| |
 \__, |\___|\__, |.
    | |      __/ |
    |_|     |___/ 

`qey` is a package to configure hotstrings with ease.
Start it by running `qey start`. Try it out by writing down anywhere '^cat'.
Run `qey --help` for more details.
"""

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
HOME = os.path.expanduser("~")
CONFIG_PATH = os.path.join(HOME, '.config')
CONFIG_QEY_PATH = os.path.join(CONFIG_PATH, 'qey')
CONFIG_FILE = os.path.join(CONFIG_QEY_PATH, 'config.json')
PIDS_PATH = os.path.join(CONFIG_QEY_PATH, 'pids')
HOTCHAR = '^'

if not os.path.isdir(CONFIG_PATH):
    os.mkdir(CONFIG_PATH)
if not os.path.isdir(CONFIG_QEY_PATH):
    os.mkdir(CONFIG_QEY_PATH)
if not os.path.isfile(CONFIG_FILE):
    DEFAULT_INI_FILE = os.path.join(CONFIG_QEY_PATH, 'hotstrings.ini').replace('\\', '/')
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        f.write('{{"INI_FILE" : "{}"}}'.format(DEFAULT_INI_FILE))
    with open(DEFAULT_INI_FILE, 'w', encoding='utf-8') as f:
        f.write('cat 😺')
if not os.path.isdir(PIDS_PATH):
    os.mkdir(PIDS_PATH)


def start():
    """Start `qey`."""
    hotstrings = get_hotstrings(CONFIG_FILE, HOTCHAR)
    hotstring_file = os.path.join(CONFIG_QEY_PATH, 'hotstrings')
    extention = '.ahk' if not is_linux() else ''
    hotstring_file += extention

    write_hotstrings(hotstrings, hotstring_file, HOTCHAR)
    if is_linux():
        hotstring_executor = os.path.join(CURRENT_PATH, "linux", "autokey_simple.py")
        cmd = '{python} {hotstring_executor} {file} &'
        cmd = cmd.format(python=sys.executable, hotstring_executor=hotstring_executor, file=hotstring_file)
    else:
        hotstring_executor = os.path.join(CURRENT_PATH, "windows", "AutoHotkey.exe")
        cmd = 'cmd.exe /C start "{hotstring_executor}" "{file}"'.format(hotstring_executor=hotstring_executor, file=hotstring_file)
    subprocess.call(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def stop():
    """Stop `qey`."""
    for file in os.listdir(PIDS_PATH):
        try:
            pid = int(file)
            p = psutil.Process(pid)
            p.terminate()
            if os.path.isfile(os.path.join(PIDS_PATH, file)):
                os.remove(os.path.join(PIDS_PATH, file))
        except Exception:
            os.remove(os.path.join(PIDS_PATH, file))


def edit():
    """Edit the hotstring file."""
    data = read_json(CONFIG_FILE)
    ini_file = data.get("INI_FILE", None)
    if ini_file is not None:
        cmd = 'xdg-open {}' if is_linux() else 'cmd.exe /C start "" "{}"'
        subprocess.call(cmd.format(ini_file), shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)


def set_file(filename: str):
    """Set the INI file containing hotstrings."""
    data = read_json(CONFIG_FILE)
    data["INI_FILE"] = os.path.abspath(filename)
    write_json(CONFIG_FILE, data)
    if os.listdir(PIDS_PATH):
        start()


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subparser_name")
    subparsers.add_parser('start', description=start.__doc__)
    subparsers.add_parser('stop', description=stop.__doc__)
    subparsers.add_parser('edit', description=edit.__doc__)
    set_file_parser = subparsers.add_parser('set_file', description=set_file.__doc__)
    set_file_parser.add_argument('path', type=str)

    args = parser.parse_args()
    if args.subparser_name == 'start':
        start()
    elif args.subparser_name == 'stop':
        stop()
    elif args.subparser_name == 'edit':
        edit()
    elif args.subparser_name == 'set_file':
        set_file(args.path)
    else:
        print(WELCOME_MESSAGE)


if __name__ == '__main__':
    main()
