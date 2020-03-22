#SingleInstance force
#Persistent
#Hotstring EndChars ,?!`n `t
#InputLevel, 1

PID:=DllCall("GetCurrentProcessId")
SplitPath, A_Desktop,,HOME
PIDS_PATH=%HOME%\.config\qey\pids
PID_FILE=%PIDS_PATH%\%PID%
FileAppend,,%PID_FILE%

OnExit("removePidFile", -1)

removePidFile(){
	global PID_FILE
	if(FileExist(PID_FILE))
	{
		FileDelete, %PID_FILE%
	}
}

