
#SingleInstance force
#Persistent
#Hotstring EndChars ,?!`n `t
#InputLevel, 1

:o?::day::
FormatTime, CurrentDateTime,, yyyy/MM/dd
SendInput %CurrentDateTime%
return

:o?::hour::
FormatTime, CurrentDateTime,, HH:mm
SendInput %CurrentDateTime%
return

:o?::time::
FormatTime, CurrentDateTime,, yyyy-MM-dd_HH-mm-ss
SendInput %CurrentDateTime%
return

:oC?:f:recap::C:/Users/qleveque/Documents/papers/recap.txt
:oC?:d:docs::C:/Users/qleveque/Documents/.
:oC?:d:papers::C:/Users/qleveque/Documents/papers/.
:oC?:d:progx::C:/Program Files (x86)
:oC?:d:macros::C:/Users/qleveque/Documents/macros/.
:oC?:i:wiki::https://bluebotics.atlassian.net
:oC?:i:deepl::https://www.deepl.com/translator
:oC?:i:jenkins::http://bluedev:8080/
:oC?:d:bb::C:/Users/qleveque/Documents/codes/BlueBotics/.
:oC?:f:todo::C:/Users/qleveque/Documents/papers/todo.txt
:oC?:d:prog::C:/Program Files
:oC?:i:gerrit::http://bluedev:8086/dashboard/self
:oC?:d:i:://igor/bluebotics
:oC?:d:mybin::C:/Users/qleveque/Documents/macros/mybin/.
:oC?:i:mail::https://workspace.infomaniak.com
:oC?:i:all::http://bluedev/
