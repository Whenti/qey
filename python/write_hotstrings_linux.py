import os, shutil
import string
import re
import stat

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

#rep = rep.replace('"', '\\"')

HOTSTRINGS_DIR = os.path.join(os.environ['HOME'],".config","autokey","data","abbr_scripts")

#create_hotkey function
def create_hotkey(abr, rep, idx):
    py_file = os.path.join(HOTSTRINGS_DIR,"{}.py".format(idx))
    json_file = os.path.join(HOTSTRINGS_DIR,".{}.json".format(idx))
    with open(py_file, "w+", encoding = "utf-8") as f:
        f.write(base_python.format(rep = rep))
    os.chmod(py_file, 0o777)
    with open(json_file, "w+", encoding = "utf-8") as f:
        f.write(base.format(abr = abr , idx = idx))
    os.chmod(json_file, 0o777)

def write_hotstrings(dico):
    #remove all
    if os.path.isdir(HOTSTRINGS_DIR):
        shutil.rmtree(HOTSTRINGS_DIR)
    os.mkdir(HOTSTRINGS_DIR)
    os.chmod(HOTSTRINGS_DIR, 0o777)

    #recreate folder_json
    FOLDER = os.path.join(HOTSTRINGS_DIR,".folder.json")
    with open(FOLDER, "w+", encoding = 'utf-8') as f:
        f.write(folder_json)
    os.chmod(FOLDER, 0o777)

    #read my hotstrings
    i=0
    char_width = 5
    for key, value in dico.items():
        idx = '{i:0>{width}}'.format(i=i,width=char_width)
        create_hotkey(key,value,idx)
        i+=1