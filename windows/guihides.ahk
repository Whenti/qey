DetectHiddenWindows, On

guihides:
    id := WinExist("ahk_class VirtualConsoleClass")
    WinHide , ahk_id %id%
    WinSet, Bottom,, ahk_id %id%
    if WinActive("ahk_id "id)
        winActivate, ahk_class Progman
    return