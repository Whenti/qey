import sys
import os, shutil
import re
import subprocess
import string
import json
import psutil
from .utils import *

whitespace_except_space = string.whitespace.replace(" ", "")

def read_json(filename):
    if os.path.isfile(filename):
        with open(filename, encoding='utf-8') as f:
            data = json.loads(f.read())
    else:
        data = {}
    return data

def add_json(file, hotstrings):
    command = file[-6]
    json_data = read_json(file)
    for key, value in json_data.items():
        hotstrings[command+HOTCHAR+key] = value.strip(whitespace_except_space)

def add_ini(file, hotstrings):
    with open(file, "r", encoding = 'utf-8') as f:
        for line in f:
            if line.strip()!="":
                line_ = line.split(" ")
                if line[0]!="[" and len(line_)>=2:
                    string = (' '.join(line_[1:])).strip(whitespace_except_space)
                    hotstrings[HOTCHAR+line_[0]]=string

def get_hotstrings():
    pattern_json = re.compile('^.*json$')
    pattern_ini = re.compile('^.*ini$')
    HOTSTRINGS = {}

    if os.path.isdir(CONFIG_PYQO_PATH):
        JSON_FILES = []
        JSON_FILES += [os.path.join(CONFIG_PYQO_PATH,file)
            for file in os.listdir(CONFIG_PYQO_PATH)
            if file!="config.json"]
            
        if os.path.isfile(CONFIG_PYQO_FILE):
            pyqo_config = read_json(CONFIG_PYQO_FILE)
            JSON_FILES += list(pyqo_config.values())

        JSON_FILES = [file for file in JSON_FILES if pattern_json.match(file)]
        for file in JSON_FILES:
            add_json(file,HOTSTRINGS)

    if os.path.isfile(CONFIG_FILE):
        config_data = read_json(CONFIG_FILE)
        if "INI_FILE" in config_data:
            INI_FILE = config_data["INI_FILE"]
            add_ini(INI_FILE, HOTSTRINGS)

    return HOTSTRINGS

def write_hotstrings(hotstrings, hotstring_file):
        if sys.platform in ['linux', 'linux2']:
            lhotstrings = {}
            for key,value in hotstrings.items():
                lhotstrings[key] = ["replace", value]
            lhotstrings[HOTCHAR+"day"] = ["run", 'datetime.now().strftime("%Y/%m/%d")']
            lhotstrings[HOTCHAR+"hour"] = ["run", 'datetime.now().strftime("%H:%M")']
            lhotstrings[HOTCHAR+"time"] = ["run", 'datetime.now().strftime("%Y-%m-%d_%H-%M-%S")']

            with open(hotstring_file, 'w') as f:
                json.dump(lhotstrings, f)

        else:
            whotstrings = hotstrings
            whotstrings[HOTCHAR+"day"] = "\nFormatTime, CurrentDateTime,, yyyy/MM/dd\nSendInput %CurrentDateTime%\nreturn"
            whotstrings[HOTCHAR+"hour"] = "\nFormatTime, CurrentDateTime,, HH:mm\nSendInput %CurrentDateTime%\nreturn"
            whotstrings[HOTCHAR+"time"] = "\nFormatTime, CurrentDateTime,, yyyy-MM-dd_HH-mm-ss\nSendInput %CurrentDateTime%\nreturn"
            with open(os.path.join(CURRENT_PATH,"windows","header.ahk")) as f:
                header_lines = f.readlines()

            with open(hotstring_file, 'w', encoding = 'utf-8') as f:
                for line in header_lines:
                    f.write(line)
                for key, value in whotstrings.items():
                    f.write(':oC?:{key}::{value}\n'.format(key=key,value=value))

def start():
    hotstrings = get_hotstrings()
    hotstring_file = os.path.join(CONFIG_QEY_PATH, 'hotstrings.ahk')
    write_hotstrings(hotstrings, hotstring_file)

    if sys.platform in ['linux', 'linux2']:
        AUTOKEY_SIMPLE = os.path.join(CURRENT_PATH,"linux","autokey_simple.py")
        cmd = '{python} {autokey_simple} {file} &'.format(python = sys.executable, autokey_simple=AUTOKEY_SIMPLE, file=hotstring_file)
        subprocess.call(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        #subprocess.call('start "" "{}"'.format(hotkeys),shell=True)
        AUTOHOTKEY = os.path.join(CURRENT_PATH,"windows","AutoHotkey.exe")
        cmd = 'start "{ahk}" "{file}"'.format(ahk = AUTOHOTKEY, file=hotstring_file)
        subprocess.call(cmd,shell=True)

def stop():
    for file in os.listdir(PIDS_PATH):
        try:
            PID = int(file)
            p = psutil.Process(PID)
            p.terminate()
            if os.path.isfile(os.path.join(PIDS_PATH,file)):
                os.remove(os.path.join(PIDS_PATH,file))
        except:
            os.remove(os.path.join(PIDS_PATH,file))

if __name__ == "__main__":
    start()
