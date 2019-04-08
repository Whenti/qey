import sys
import subprocess
import os

def start():
    current_path = os.path.dirname(os.path.abspath(__file__))

    if sys.platform in ['linux', 'linux2']:
        pass
    else:
        hot = os.path.join(current_path, 'windows', 'hot.ahk')
        subprocess.call('open {}'.format(hot),shell=True)
    
if __name__ == "__main__":
    start()