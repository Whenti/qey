import sys
import os

from .utils import *

def setstartup():
    if sys.platform in ['linux', 'linux2']:
        content_flag = "#QEY_START"
        add_profile = """
#QEY_START
qey start
#QEY_END
    """.format(python=sys.executable, start=os.path.join(CURRENT_PATH,"start.py"))

        def addLines(filename, content, add):
            with open(filename, "r+") as file:
                for line in file:
                    if content in line:
                        return
                file.write(add)
        addLines("{}/.profile".format(os.environ['HOME']), content_flag, add_profile)

    else:
        #set starting script in shell:startup
        from win32com.shell import shell, shellcon
        startup_dir = shell.SHGetFolderPath(0,shellcon.CSIDL_STARTUP,0,0)
        with open(os.path.join(startup_dir,"start_qey.bat"),"w",encoding='utf-8') as f:
            f.write("qey start")
