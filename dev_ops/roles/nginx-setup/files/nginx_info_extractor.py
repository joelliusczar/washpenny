import re
import subprocess
import os

def get_nginx_value(key: str = "conf-path"):
	proc = subprocess.Popen([
			"/usr/sbin/nginx",
			"-V",
		],
		stdout=subprocess.PIPE,
		text=True
	)
	out, _ = proc.communicate()
	for segment in out.split():
		if match := re.match(fr"--{key} *= *(.*)",segment):
			return match.group(1)
	return ""

def get_nginx_conf_dir_include(nginxConfPath: str=""):
	if not nginxConfPath:
		nginxConfPath = get_nginx_value()
	guesses = [
		"include /etc/nginx/sites-enabled/*;",
		"include servers/*;"
	]
	configContent = open(nginxConfPath).read()
	for guess in guesses:
		if guess in configContent:
			return guess
	return ""

def get_abs_path_from_nginx_include(confDirInclude: str=""):
	if not confDirInclude:
		confDirInclude = get_nginx_conf_dir_include()
	confDir = confDirInclude\
		.replace("include ","")\
		.replace("*/;","")\
		.strip()
	
	if os.path.isdir(confDir):
		return confDir
	else:
		nginxConfPath = get_nginx_value()
		sitesFolderPath = os.path.dirname(nginxConfPath)
		absPath = os.path.join(sitesFolderPath, confDir)
		if not os.path.isdir(absPath):
			if os.path.exists(absPath):
				raise RuntimeError(f"{absPath} is a file, not a directory")
			
			os.makedirs(absPath, exist_ok=True)
		return absPath


