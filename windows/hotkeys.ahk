#SingleInstance force
#Persistent
#Hotstring EndChars ,?!`n `t
#InputLevel, 1
DetectHiddenWindows, On

SetWorkingDir, %A_ScriptDir%

CONSOLE := "VirtualConsoleClass"

#include %A_ScriptDir%\guihides.ahk
#include %A_ScriptDir%\guishow.ahk

;#################### hotstrings

;----------------------------LALT
<!Backspace::SendInput, {Delete}
<!Space::
    If !WinActive("ahk_class VirtualConsoleClass")
    {
        gosub guishow
        return
    }
    gosub guihides
	return

;-------------------------NAVIGATION

<!i::SendInput, {Up}
<!j::SendInput, {Left}
<!k::SendInput, {Down}
<!l::SendInput, {Right}
<!h::SendInput, {Home}
<!m::SendInput, {End}
<!o::SendInput, {CTRL DOWN}{RIGHT}{CTRL UP}
<!u::SendInput, {CTRL DOWN}{LEFT}{CTRL UP}
Virgule:
	; SendInput, {PgUp}
    SendInput, {Up 20}
	return
DeuxPoints:
	; SendInput, {PgDn}
    SendInput, {Down 20}
	return
!+i::SendInput, {Shift Down}{Up}{Shift Up}
!+j::SendInput, {Shift Down}{Left}{Shift Up}
!+k::SendInput, {Shift Down}{Down}{Shift Up}
!+l::SendInput, {Shift Down}{Right}{Shift Up}
!+h::SendInput, {Shift Down}{Home}{Shift Up}
!+m::SendInput, {Shift Down}{End}{Shift Up}
!+o::SendInput, {Shift Down}{CTRL DOWN}{RIGHT}{CTRL UP}{Shift Up}
!+u::SendInput, {Shift Down}{CTRL DOWN}{LEFT}{CTRL UP}{Shift Up}
SVirgule:
	; SendInput, {Shift Down}{PgUp}{Shift Up}
    SendInput, {Shift Down}{Up 20}{Shift Up}
	return
SDeuxPoints:
	; SendInput, {Shift Down}{PgDn}{Shift Up}
    SendInput, {Shift Down}{Down 20}{Shift Up}
	return

!;::SendInput, {Insert}