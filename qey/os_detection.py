import platform

def is_linux():
    if platform.system()=='Windows':
        return False
    if 'microsoft' in platform.uname()[3].lower():
        return False
    return True
