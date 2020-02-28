#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The ``hotkeys_handling`` module
======================
Contains all the functions related to the reading and modifications of the hotstring file.
"""
import sys
import re
import string
import json
import os

from typing import Dict

from qey import json_handling

PYQO_DIR = os.path.join(os.path.expanduser("~"), '.config', 'pyqo')
WHITESPACE_EXCEPT_SPACE = string.whitespace.replace(" ", "")


def hotstrings_from_json(file: str, hot_char: str):
    hotstrings = {}
    command = file[-6]
    json_data = json_handling.read_json(file)
    for key, value in json_data.items():
        hotstrings[command + hot_char + key] = value.strip(WHITESPACE_EXCEPT_SPACE)
    return hotstrings


def hotstrings_from_ini(file: str, hot_char: str):
    hotstrings = {}
    with open(file, "r", encoding='utf-8') as f:
        for line in f:
            if line.strip() != "" and line[0] != "[":
                line_ = line.split(" ")
                if len(line_) >= 2:
                    replacement = (' '.join(line_[1:])).strip(WHITESPACE_EXCEPT_SPACE)
                    hotstrings[hot_char + line_[0]] = replacement
    return hotstrings


def get_hotstrings(config_file: str, hot_char: str):
    hotstrings = {}
    if os.path.isdir(PYQO_DIR):
        json_files = []
        for file in os.listdir(PYQO_DIR):
            if file != "config.json":
                json_files.append(os.path.join(PYQO_DIR, file))
        pyqo_config = json_handling.read_json(os.path.join(PYQO_DIR, 'config.json'))
        json_files += list(pyqo_config.values())
        pattern_json = re.compile('^.*json$')
        json_files = [file for file in json_files if pattern_json.match(file)]
        for file in json_files:
            hotstrings.update(hotstrings_from_json(file, hot_char))

    # adding files from the ini file
    config_data = json_handling.read_json(config_file)
    ini_file = config_data.get("INI_FILE", None)
    if ini_file is not None:
        hotstrings.update(hotstrings_from_ini(ini_file, hot_char))
    else:
        hotstrings.update()

    return hotstrings


def write_hotstrings(hotstrings: Dict[str, str], hotstring_file: str, hot_char: str):
    if sys.platform in ['linux', 'linux2']:
        hotstring_commands = {}
        for key, value in hotstrings.items():
            hotstring_commands[key] = ["replace", value]
        hotstring_commands[hot_char + "day"] = ["run", 'datetime.now().strftime("%Y/%m/%d")']
        hotstring_commands[hot_char + "hour"] = ["run", 'datetime.now().strftime("%H:%M")']
        hotstring_commands[hot_char + "time"] = ["run", 'datetime.now().strftime("%Y-%m-%d_%H-%M-%S")']

        with open(hotstring_file, 'w') as f:
            json.dump(hotstring_commands, f)

    else:
        current_path = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(current_path, "windows", "header.ahk")) as f:
            header_lines = f.readlines()

        with open(hotstring_file, 'w', encoding='utf-8') as f:
            f.write('\ufeff')
            for line in header_lines:
                f.write(line)
            f.write(':oC?:day::\nFormatTime, CurrentDateTime,, yyyy/MM/dd\nSendInput %CurrentDateTime%\nreturn\n')
            f.write(':oC?:hour::\nFormatTime, CurrentDateTime,, HH:mm\nSendInput %CurrentDateTime%\nreturn\n')
            f.write(':oC?:time::\nFormatTime, CurrentDateTime,,' +
                    'yyyy-MM-dd_HH-mm-ss\nSendInput %CurrentDateTime%\nreturn\n')

            form = ':{param}:{key}::\nSendInput, {value}\nreturn\n'

            for key, value in hotstrings.items():
                if key[-1] == ':':
                    for sep in [" ", "`t", "`n"]:
                        f.write(form.format(key=key+sep, value=value, param="oC?*"))
                else:
                    f.write(form.format(key=key, value=value, param="oC?"))
