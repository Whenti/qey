import os, shutil
import string
import re
import sys
from _reader import *

current_dir = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(current_dir, "..", "data")
CONFIG = read_json(os.path.join(current_dir, "..", "config.json"))

whitespace_except_space = string.whitespace.replace(" ", "")

PATHS = list(CONFIG.values())
HOTSTRINGS = {}

def set_hotstrings():
    for PATH in PATHS:
        files = os.listdir(PATH)
        pattern_json = re.compile('^.*json$')
        pattern_ini = re.compile('^.*ini$')
        for file in files:
            #json files
            if pattern_json.match(file):
                command = file[:-5]
                json_data = read_json(os.path.join(PATH,file))
                for key, value in json_data.items():
                    HOTSTRINGS[command+':'+key] = value.strip(whitespace_except_space)

            #ini files
            elif pattern_ini.match(file):
                with open(os.path.join(PATH, file), "r", encoding = 'utf-8') as f:
                    for line in f:
                        if line.strip()!="":
                            line_ = line.split(" ")
                            if line[0]!="[" and len(line_)>=2:
                                string = (' '.join(line_[1:])).strip(whitespace_except_space)
                                HOTSTRINGS[':'+line_[0]]=string

    if sys.platform in ['linux', 'linux2']:
        from write_hotstrings_linux import write_hotstrings
    else:
        from write_hotstrings_windows import write_hotstrings

    write_hotstrings(HOTSTRINGS)

if __name__ == "__main__":
    set_hotstrings()
