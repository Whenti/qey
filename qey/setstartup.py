import sys
import os

from .utils import *

def addLine(filename, add):
    with open(filename, "r+") as file:
        for line in file:
            if cmd in line:
                return
        file.write(cmd)

def removeLine(filename, cmd):
    with open(filename, "r+") as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            if i != cmd:
                f.write(i)
        f.truncate()

def setstartup(set):
    if sys.platform in ['linux', 'linux2']:
        PROFILE = "{}/.profile".format(os.environ['HOME'])
        cmd = "qey start"
        if set:
            addLine(PROFILE, cmd)
        else:
            removeLine(PROFILE, cmd)

    else:
        #set starting script in shell:startup
        from win32com.shell import shell, shellcon
        startup_dir = shell.SHGetFolderPath(0,shellcon.CSIDL_STARTUP,0,0)
        START_FILE = os.path.join(startup_dir,"start_qey.bat")
        if set:
            with open(START_FILE,"w",encoding='utf-8') as f:
                f.write("qey start")
        else:
            os.remove(START_FILE)
        
