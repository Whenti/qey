DetectHiddenWindows, On

guishow:
    id := WinExist("ahk_class VirtualConsoleClass")
    if(id)
    {
        WinShow, ahk_id %id%
        WinActivate, ahk_id %id%
    }
    else
        run, C:\Program Files\ConEmu\ConEmu64.exe, C:\Users\Whenti
    return