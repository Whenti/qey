import os

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
HOME = os.path.expanduser("~")
CONFIG_PATH = os.path.join(HOME,'.config')
CONFIG_QEY_PATH = os.path.join(CONFIG_PATH,'qey')
CONFIG_PYQO_PATH = os.path.join(CONFIG_PATH,'pyqo')
CONFIG_FILE = os.path.join(CONFIG_QEY_PATH, 'config.json')
CONFIG_PYQO_FILE = os.path.join(CONFIG_PYQO_PATH, 'config.json')
PIDS_PATH = os.path.join(CONFIG_QEY_PATH,'pids')
HOTCHAR = '^'
