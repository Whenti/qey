import sys
import subprocess
import os
from set_hotstrings import *

def start():
    set_hotstrings()

    current_path = os.path.dirname(os.path.abspath(__file__))

    if sys.platform in ['linux', 'linux2']:
        subprocess.call('autokey &', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        hotkeys = os.path.join(current_path, 'windows', 'hotkeys.ahk')
        subprocess.call('open {}'.format(hotkeys),shell=True)
        hotstrings = os.path.join(current_path, 'windows', 'hotstrings.ahk')
        if os.file.exists(hotstrings):
            subprocess.call('open {}'.format(hotstrings),shell=True)


if __name__ == "__main__":
    start()
