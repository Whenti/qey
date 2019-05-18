import sys
import subprocess
import os
from shutil import copyfile

current_path = os.path.dirname(os.path.abspath(__file__))

os.chdir(current_path)
sys.path.append('qey')

from start import start

HOME = os.path.expanduser("~")
CONFIG_PATH = os.path.join(HOME,'.config')
QEY_PATH = os.path.join(CONFIG_PATH,'qey')
CONFIG_FILE = os.path.join(QEY_PATH,'config.json')

if not os.path.isdir(CONFIG_PATH):
    os.mkdir(QEY_PATH)
if not os.path.isdir(QEY_PATH):
    os.mkdir(CONFIG_PATH)
if not os.path.isfile(CONFIG_FILE):
    with open(CONFIG_FILE,'w',encoding='utf-8') as f:
        f.write('{"PATHS" : []}')
    

if sys.platform in ['linux', 'linux2']:
    #make autokey start automatically
    content_flag = "#QEY_START"
    add_profile = """
#QEY_START
python3 {}
#QEY_END
""".format(os.path.join(current_path,"python","start.py"))

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
        file_to_start = os.path.join(current_path,"python","start.py")
        f.write("python {}".format(file_to_start))

start()
