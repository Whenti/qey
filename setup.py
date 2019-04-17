import sys
import subprocess
import os
from shutil import copyfile

sys.path.append('python')

from start import *

current_path = os.path.dirname(os.path.abspath(__file__))

HOME = os.path.expanduser("~")
CONFIG = os.path.join(HOME,'.config')
QEY_PATH = os.path.join(CONFIG,'qey')

if not os.path.isdir(CONFIG_PATH):
    os.mkdir(CONFIG_PATH)
if not os.path.isdir(QEY_PATH):
    os.mkdir(QEY_PATH)

def addLines(filename, content, add):
    with open(filename, "r+") as file:
        for line in file:
            if content in line:
                return
        file.write(add)

if sys.platform in ['linux', 'linux2']:
    #setup wh keyboard
    KEYBOARD = os.path.join(current_path,'linux','keyboard')
    XKB = "/usr/share/X11/xkb"
    copyfile(os.path.join(KEYBOARD,'wh'), os.path.join(XKB,'symbols','wh'))
    copyfile(os.path.join(KEYBOARD,'evdev.xml'), os.path.join(XKB,'rules','evdev.xml'))

    #setup space autokey
    HOTKEYS = os.path.join(current_path, 'linux','hotkeys')
    with open(os.path.join(HOTKEYS,'space.py'), 'w', encoding='utf-8') as f:
        terminal_pop = os.path.join(current_path,"linux","terminal_pop.sh")
        to_write = "import os\nos.system('sh {}')".format(terminal_pop)
        f.write(to_write)

    #setup autokey
    AUTOKEY_DATA = os.path.join(os.environ['HOME'],'.config','autokey','data')
    os.system("cp -r {hotkeys} {autokey_data}".format(hotkeys = HOTKEYS, autokey_data=AUTOKEY_DATA))

    #make autokey start automatically
    content_flag = "#QEY_START"
    add_profile = """
#QEY_START
python3 {}
#QEY_END
""".format(os.path.join(current_path,"python","start.py"))
    addLines("{}/.profile".format(os.environ['HOME']), content_flag, add_profile)

else:
    #set starting script in shell:startup
    from win32com.shell import shell, shellcon
    startup_dir = shell.SHGetFolderPath(0,shellcon.CSIDL_STARTUP,0,0)
    with open(os.path.join(startup_dir,"start_qey.bat"),"w",encoding='utf-8') as f:
        file_to_start = os.path.join(current_path,"python","start.py")
        f.write("python {}".format(file_to_start))

start()
