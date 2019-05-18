import os

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
HOME = os.path.expanduser("~")
CONFIG_PATH = os.path.join(HOME,'.config')
CONFIG_QEY_PATH = os.path.join(CONFIG_PATH,'qey')
CONFIG_PYQO_PATH = os.path.join(CONFIG_PATH,'pyqo')
HOTCHAR = '^'
