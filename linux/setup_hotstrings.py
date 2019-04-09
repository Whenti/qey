import keyboard as kb
import os, shutil
import string
import random
from configparser import ConfigParser

current_dir = os.path.dirname(os.path.abspath(__file__))

#basic of autokey file
folder_json = """{
    "usageCount": 0,
    "abbreviation": {
        "wordChars": "[^ \\\\r\\\\n]",
        "abbreviations": [],
        "immediate": false,
        "ignoreCase": false,
        "backspace": true,
        "triggerInside": false
    },
    "title": "abbr_scripts",
    "hotkey": {
        "hotKey": null,
        "modifiers": []
    },
    "filter": {
        "regex": null,
        "isRecursive": false
    },
    "type": "folder",
    "showInTrayMenu": false
}
"""

base = """{{
    "usageCount": 0,
    "omitTrigger": true,
    "prompt": false,
    "description": "{idx}",
    "abbreviation": {{
        "wordChars": "[^ \\\\r\\\\n]",
        "abbreviations": [
            "{abr}"
        ],
        "immediate": false,
        "ignoreCase": false,
        "backspace": true,
        "triggerInside": true
    }},
    "hotkey": {{
        "hotKey": null,
        "modifiers": []
    }},
    "modes": [
        1
    ],
    "showInTrayMenu": false,
    "matchCase": true,
    "filter": {{
        "regex": null,
        "isRecursive": false
    }},
    "type": "script",
    "store" : {{}}
}}"""

base_python = """
clipboard.fill_clipboard(u"{rep}")
keyboard.send_keys('<ctrl>+v')
"""

def id_generator(size=8, chars=string.ascii_uppercase):
    return ''.join(random.choice(chars) for _ in range(size))

pyqo_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")

#paths
my_hotstrings = os.path.join(pyqo_path,"data/hotstrings.ini")
data_ini = os.path.join(pyqo_path,"data/data.ini")
autokey_dir = "/home/whenti/.config/autokey/data/abbr_scripts"

#remove all
if os.path.isdir(autokey_dir):
    shutil.rmtree(autokey_dir)
os.mkdir(autokey_dir)

#recreate folder_json
folder_filename = os.path.join(autokey_dir,".folder.json")
with open(folder_filename, "w", encoding = 'utf-8') as f:
    f.write(folder_json)

#simplify
def simplify(rep):
    rep = rep.replace('"', '\\"')
    rep = rep.replace("\n", "")
    rep = rep.replace("\r", "")
    return rep
#create_hotkey function
def create_hotkey(abr, rep, idx):
    abr = simplify(abr)
    rep = simplify(rep)
    py_file = os.path.join(autokey_dir,"{}.py".format(idx))
    json_file = os.path.join(autokey_dir,".{}.json".format(idx))
    with open(py_file, "w", encoding = "utf-8") as f:
        f.write(base_python.format(rep = rep))
    with open(json_file, "w", encoding = "utf-8") as f:
        f.write(base.format(abr = abr , idx = idx))

#read my hotstrings
with open(my_hotstrings, "r", encoding = 'utf-8') as f:
    hotstrings = {}
    for line in f:
        if line.strip()!="":
            line_ = line.split(" ")
            if line[0]!="[" and len(line_)>=2:
                hotstrings[':'+line_[0]]=' '.join(line_[1:])

    f = ConfigParser()
    with open(data_ini, 'r', encoding='utf-8') as to_read:
        f.read_file(to_read)
    d = {}
    for section in f.sections():
        if "_windows" not in section:
            sec = section.replace("_linux","")
            for key, value in f.items(section):
                hotstrings[sec+":"+key] = value
    char_width = 5
    #i = len(list(hotstrings))
    i=0
    for key in sorted(hotstrings):
        idx = '{i:0>{width}}'.format(i=i,width=char_width)
        print(key)
        create_hotkey(key,hotstrings[key],idx)
