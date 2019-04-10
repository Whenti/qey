import os

current_path = os.path.dirname(os.path.abspath(__file__))
HOTSTRINGS_FILE = os.path.join(current_path,"..","windows","hotstrings.ahk")

def write_hotstrings(dico):
    with open(HOTSTRINGS_FILE, 'w', encoding = 'utf-8') as f:
        for key, value in dico.items():
            f.write(':oC:{key}::{value}\n'.format(key=key,value=value))
