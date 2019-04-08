import sys
import subprocess
import os
from start import *

current_path = os.path.dirname(os.path.abspath(__file__))

if sys.platform in ['linux', 'linux2']:
    pass
else:
    from win32com.shell import shell, shellcon
    startup_dir = shell.SHGetFolderPath(0,shellcon.CSIDL_STARTUP,0,0)
    with open(os.path.join(startup_dir,"start_qey.bat"),"w",encoding='utf-8') as f:
        file_to_start = os.path.join(current_path,'start.py')
        f.write("python {}".format(file_to_start))
        
start()