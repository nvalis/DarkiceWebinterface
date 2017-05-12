from flask import render_template, flash, redirect, request
from app import app, darkice_handler
from .forms import ConfigForm

from darkice import *

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
	output = ''
	if request.method == 'POST':
		if request.form['submit'] == 'Start':
			darkice_handler.start()
		elif request.form['submit'] == 'Stop':
			darkice_handler.stop()
	darkice_handler.read()
	return render_template("index.html", title='Home', darkice_running=darkice_handler.running(), refresh_delay=3, output=darkice_handler.output)

@app.route('/generate_config', methods=['GET', 'POST'])
def generate_config():
	form = ConfigForm()
	if form.validate_on_submit():
		config_dict = {}
		for field in form:
			fid = field.label.field_id
			if fid in ['configfile_path', 'csrf_token']: continue
			config_dict[fid] = field.data
		generate_config_file(config_dict, file_name=str(form.configfile_path.data))

		flash('Config written to "{}"'.format(form.configfile_path.data))
	return render_template('generate_config.html', title='Configuration', form=form)

@app.route('/show_config')
def show_config():
	return render_template('show_config.html', config=read_config_file())