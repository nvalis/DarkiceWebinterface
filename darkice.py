# -*- coding: utf-8 -*-

import os
import subprocess
import configparser

def get_darkice_process_id():
	pipe = subprocess.Popen('pidof darkice', shell=True, stdout=subprocess.PIPE).stdout
	return pipe.read()

def get_darkice_status():
	pid = get_darkice_process_id()
	print(pid)
	if pid:
		return 'Running'
	else:
		return 'Not running'

def generate_config_file(config_dict, file_name='darkice.conf'):
	config = configparser.ConfigParser()
	config.optionxform=str # to preserve case: http://stackoverflow.com/a/1611877

	sections = {
		'general':['duration', 'bufferSecs', 'reconnect'],
		'input':['device', 'sampleRate', 'bitsPerSample', 'channel'],
		'icecast2-0':['format', 'bitrateMode', 'bitrate', 'quality', 'server', 'port', 'password', 'mountPoint']
	}
	for section, fields in sections.items():
		print(fields)
		config[section] = {field:config_dict[field] for field in fields}

	with open(os.path.join('app/configs/', file_name), 'w') as configfile:
		config.write(configfile)

def read_config_file(file_name='darkice.conf'):
	return open(os.path.join('app/configs/', file_name)).read()