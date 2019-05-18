import sys
import os, shutil
import re
import subprocess
import string
import json

whitespace_except_space = string.whitespace.replace(" ", "")

def read_json(filename):
	if os.path.isfile(filename):
		with open(filename, encoding='utf-8') as f:
			data = json.loads(f.read())
	else:
		data = {}
	return data

def get_hotstrings():
	PATHS = [CONFIG_QEY_PATH]
	if os.path.isdir(CONFIG_PYQO_PATH):
		PATHS.append(CONFIG_PYQO_PATH)
	config_data = read_json(os.path.join(CONFIG_QEY_PATH, 'config.json'))
	if "PATHS" in config_data:
		PATHS = PATHS + config_data["PATHS"]

	pattern_json = re.compile('^.*json$')
	pattern_ini = re.compile('^.*ini$')
	HOTSTRINGS = {}

	for PATH in PATHS:
		files = os.listdir(PATH)
		for file in files:
			if PATH==CONFIG_QEY_PATH and file=="config.json":
				continue
			#json files
			if pattern_json.match(file):
				command = file[:-5]
				json_data = read_json(os.path.join(PATH,file))
				for key, value in json_data.items():
					HOTSTRINGS[command+':'+key] = value.strip(whitespace_except_space)

			#ini files
			if pattern_ini.match(file):
				with open(os.path.join(PATH, file), "r", encoding = 'utf-8') as f:
					for line in f:
						if line.strip()!="":
							line_ = line.split(" ")
							if line[0]!="[" and len(line_)>=2:
								string = (' '.join(line_[1:])).strip(whitespace_except_space)
								HOTSTRINGS[HOTCHAR+line_[0]]=string

	return HOTSTRINGS

def write_hotstrings(hotstrings, hotstring_file):
		if sys.platform in ['linux', 'linux2']:
			lhotstrings = {}
			for key,value in hotstrings.items():
				lhotstrings[key] = ["replace", value]
			lhotstrings[HOTCHAR+"day"] = ["run", 'datetime.now().strftime("%Y/%m/%d")']
			lhotstrings[HOTCHAR+"hour"] = ["run", 'datetime.now().strftime("%H:%M")']
			lhotstrings[HOTCHAR+"time"] = ["run", 'datetime.now().strftime("%Y-%m-%d_%H-%M-%S")']

			with open(hotstring_file, 'w') as f:
				json.dump(lhotstrings, f)

		else:
			whotstrings = hotstrings
			whotstrings[HOTCHAR+"day"] = "\nFormatTime, CurrentDateTime,, yyyy/MM/dd\nSendInput %CurrentDateTime%\nreturn"
			whotstrings[HOTCHAR+"hour"] = "\nFormatTime, CurrentDateTime,, HH:mm\nSendInput %CurrentDateTime%\nreturn"
			whotstrings[HOTCHAR+"time"] = "\nFormatTime, CurrentDateTime,, yyyy-MM-dd_HH-mm-ss\nSendInput %CurrentDateTime%\nreturn"
			start_ahk_script = "\ufeff\n#SingleInstance force\n#Persistent\n#Hotstring EndChars ,?!`n `t\n#InputLevel, 1\n"

			with open(hotstring_file, 'w', encoding = 'utf-8') as f:
				f.write(start_ahk_script)
				for key, value in whotstrings.items():
					f.write(':oC?:{key}::{value}\n'.format(key=key,value=value))

def start():
	hotstrings = get_hotstrings()
	hotstring_file = os.path.join(CONFIG_QEY_PATH, 'hotstrings.ahk')
	write_hotstrings(hotstrings, hotstring_file)

	if sys.platform in ['linux', 'linux2']:
		AUTOKEY_SIMPLE = os.path.join(CURRENT_PATH,"linux","autokey_simple.py")
		cmd = '{python} {autokey_simple} {file} &'.format(python = sys.executable, autokey_simple=AUTOKEY_SIMPLE, file=hotstring_file)
		#subprocess.call(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		subprocess.call(cmd, shell=True)
	else:
		#subprocess.call('start "" "{}"'.format(hotkeys),shell=True)
		hotstrings = os.path.join(CONFIG_QEY_PATH, 'hotstrings.ahk')
		if os.path.isfile(hotstrings):
			subprocess.call('start "" "{}"'.format(hotstrings),shell=True)

if __name__ == "__main__":
	start()
