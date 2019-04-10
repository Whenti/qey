#SingleInstance force
#Persistent
#Hotstring EndChars ,?!`n `t
#InputLevel, 1
DetectHiddenWindows, On

SetWorkingDir, %A_ScriptDir%

style:=0

styles:=["Abbr.","Maj."]
text:="Loading Qey"

WinGetTitle, WorkingWindowBeforeHotkeyClass, A
gosub createGui
WinActivate, %WorkingWindowBeforeHotkeyClass%

pre_mv =

CONSOLE := "VirtualConsoleClass"

readHotstrings()

Hotkey,!`,,Virgule
Hotkey,!:,DeuxPoints
Hotkey,!+`,,SVirgule
Hotkey,!+:,SDeuxPoints

return

#include %A_ScriptDir%\guihides.ahk
#include %A_ScriptDir%\guishow.ahk

updateGui:
    Gui, Hide
    if(style!=0)
    {
        text:=styles[style]

        GuiControl,,Text, %text%
        GuiControl, +Center, Text
        Gui, Show, NA, AlwaysOnTop Window
    }
    return

createGui:
    CoordMode, Pixel, Screen
    Gui, Font, s10 cFFFFFF Bold, Verdana
    Gui, -Caption +E0x200 +ToolWindow
    Gui, Color, 0x4D4D4D
    Gui, Add, Text, vText, %text%
    Gui, Show
    WinGet, k_ID, ID, A
    WinSetTitle, ahk_id %k_ID%,,__Qey__
    WinGetPos,,, k_WindowWidth, k_WindowHeight, A
    SysGet, k_WorkArea, MonitorWorkArea
    k_WindowX := (k_WorkAreaRight-k_WorkAreaLeft-k_WindowWidth+k_WorkAreaLeft)/2
    k_WindowY := (k_WorkAreaBottom-k_WindowHeight)/2
    WinMove, A,, %k_WindowX%, 0
    WinSet, TransColor, F1ECED 200, ahk_id %k_ID%
    WinSet, AlwaysOnTop, On, ahk_id %k_ID%
    Gui, Hide
return

;#################### hotkeys

:o::day.::
FormatTime, CurrentDateTime,, yyyy.MM.dd
SendInput %CurrentDateTime% `
return
:o::day_::
FormatTime, CurrentDateTime,, yyyy_MM_dd
SendInput %CurrentDateTime% `
return
:o::day::
FormatTime, CurrentDateTime,, yyyy/MM/dd
SendInput %CurrentDateTime% `
return

:o::hour::
FormatTime, CurrentDateTime,, HH:mm
SendInput %CurrentDateTime% `
return
:o::hour_::
FormatTime, CurrentDateTime,, HH_mm
SendInput %CurrentDateTime% `
return
:o::hour.::
FormatTime, CurrentDateTime,, HH.mm
SendInput %CurrentDateTime% `
return

;#################### hotstrings

;----------------------------LALT
<!Backspace::SendInput, {Delete}
<!Enter::Send ^{Enter} ; for google search
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

;-------------------CTRL
$^q::
	WinGetClass, class, A
    if(class="CabinetWClass")
    {
        Send, !{F4}
    }
	else if(class!=CONSOLE)
    {
		PostMessage, 0x112, 0xF060,,,A
    }
	return
$+^q::
	WinClose, A
	return

$^e::
    WinGetClass, class, A
    if(class="CabinetWClass")
    {
        obj:=ComObjCreate("QTTabBarLib.Scripting")
        ; dir:=obj.CurrentDirectory
        dir:=obj.ActiveWindow.ActiveTab.Path()
        obj.ActiveWindow.ActiveTab.Close()
        obj.OpenWindow(dir)
        return
    }
    Send, ^e
    return

$^l::
    WinGetClass, class, A
    if(class="PX_WINDOW_CLASS")
        Send, ^b
    else if(class="wxWindowClassNR")
        Send, {F9}
    else if(class="CabinetWClass")
    {
        ControlFocus, ToolbarWindow322, A
        Send, {Space}
    }
    else if(class="#32770")
    {
        ControlFocus, ToolbarWindow323, A
        Send, {Space}
    }
    Else
        Send ^l
    return

;----------------------------LAYOUT (normal maj ralt)
$²::Send {Escape}
$+&::Send ‽
$+é::Send É
$+"::Send ¦ ;"
$+è::Send È
$+ç::Send Ç
$+à::Send À
$+_::Send -
$+'::Send |
$+(::Send {U+00A0}
$-::Send –
$+-::Send ―
*$PrintScreen::Run SnippingTool.exe

$<^>!<::Send «
$<^>!+<::Send »
;----------------------------RALT
<^>!q:: Send, {Numpad1}
<^>!s:: Send, {Numpad2}
<^>!d:: Send, {Numpad3}
<^>!f:: Send, {Numpad4}
<^>!g:: Send, {Numpad5}
<^>!h:: Send, {Numpad6}
<^>!j:: Send, {Numpad7}
<^>!k:: Send, {Numpad8}
<^>!l:: Send, {Numpad9}
<^>!m:: Send, {Numpad0}
;------------------more
<^>!+o::Send Œ
<^>!+a::Send Æ
<^>!x::Send ×
<^>!c::Send ©
<^>!b::Send ß
<^>!p::Send ¶
<^>!o::Send œ
<^>!a::Send æ
<^>!.::Send .
<^>!,::Send `,
<^>!Space::Send {Space}


;------------MAJ
$CapsLock::
if(style=2)
	style:=0
else
	style:=2
gosub updateGui
return

#If style=2
<^>!a::Æ
<^>!o::Œ
:*?o:ê::Ê
:*?o:ë::Ë
:*?o:û::Û
:*?o:î::Î
:*?o:œ::Œ
:*?o:æ::Æ
:*?o:a::A
:*?o:b::B
:*?o:c::C
:*?o:d::D
:*?o:e::E
:*?o:f::F
:*?o:g::G
:*?o:h::H
:*?o:i::I
:*?o:j::J
:*?o:k::K
:*?o:l::L
:*?o:m::M
:*?o:n::N
:*?o:o::O
:*?o:p::P
:*?o:q::Q
:*?o:r::R
:*?o:s::S
:*?o:t::T
:*?o:u::U
:*?o:v::V
:*?o:w::W
:*?o:x::X
:*?o:y::Y
:*?o:z::Z
:*?o:ç::Ç
:*?o:à::À
:*?o:é::É
:*?o:è::È
:*?o:ù::Ù


#If
