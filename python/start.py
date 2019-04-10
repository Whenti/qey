import sys
import subprocess
import os
from set_hotstrings import *

QEY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')

def start():
    set_hotstrings()

    if sys.platform in ['linux', 'linux2']:
        subprocess.call('autokey &', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        hotkeys = os.path.join(QEY_PATH, 'windows', 'hotkeys.ahk')
        subprocess.call('open {}'.format(hotkeys),shell=True)
        hotstrings = os.path.join(QEY_PATH, 'windows', 'hotstrings.ahk')
        if os.path.isfile(hotstrings):
            subprocess.call('open {}'.format(hotstrings),shell=True)


if __name__ == "__main__":
    start()