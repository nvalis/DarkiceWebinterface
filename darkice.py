# -*- coding: utf-8 -*-

import os
import subprocess
import shlex
import configparser
import fcntl

class DarkiceHandler:
	def __init__(self, config_file_name='darkice.conf'):
		self.set_config(config_file_name)
		self.process = None
		self.output = '--- Initialized'

	def set_config(self, config_file_name):
		fp = os.path.join('app/configs/', config_file_name)
		fp = shlex.quote(fp) # get shell-escaped version
		if not os.path.isfile(fp):
			print('Could not find: \'{}\''.format(fp))
		else:
			self.config_file_path = fp

	def running(self):
		return bool(self.process)

	def start(self):
		if not self.process:
			self.log('--- Starting process...')
			self.process = subprocess.Popen('darkice -c {}'.format(self.config_file_path), shell=True, stdout=subprocess.PIPE)
			fcntl.fcntl(self.process.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK) # http://stackoverflow.com/a/8980466
		else:
			print('Process already started!')

	def stop(self):
		if self.process:
			self.process.terminate()
			self.process = None
			self.log('--- Stopped process.')
		else:
			print('No process to stop!')

	def log(self, message):
		self.output += '\n' + message

	def read(self):
		if self.process:
			try:
				out = self.process.stdout.read()
				if out: self.log(out.decode())
			except IOError: # no new output
				pass


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