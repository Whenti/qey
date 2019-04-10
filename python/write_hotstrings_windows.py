import os

current_path = os.path.dirname(os.path.abspath(__file__))
HOTSTRINGS_FILE = os.path.join(current_path,"..","windows","hotstrings.ahk")

START = """\ufeff
#SingleInstance force
#Persistent
#Hotstring EndChars ,?!`n `t
#InputLevel, 1

:o?::day::
FormatTime, CurrentDateTime,, yyyy/MM/dd
SendInput %CurrentDateTime%
return

:o?::hour::
FormatTime, CurrentDateTime,, HH:mm
SendInput %CurrentDateTime%
return

:o?::time::
FormatTime, CurrentDateTime,, yyyy-MM-dd_HH-mm-ss
SendInput %CurrentDateTime%
return

"""

def write_hotstrings(dico):
    with open(HOTSTRINGS_FILE, 'w', encoding = 'utf-8') as f:
        f.write(START)
        for key, value in dico.items():
            f.write(':oC?:{key}::{value}\n'.format(key=key,value=value))