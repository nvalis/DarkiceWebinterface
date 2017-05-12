from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SelectField, DecimalField
from wtforms.validators import DataRequired, NumberRange

class ConfigForm(FlaskForm):
	# general
	duration = IntegerField(
		'Encoding duration',
		description='Duration of encoding in seconds. 0 means forever',
		default=0
	)
	bufferSecs = IntegerField(
		'Buffer size',
		description='Size of internal slip buffer in seconds.',
		default=5,
		validators=[DataRequired()]
	)
	reconnect = BooleanField(
		'Reconnect',
		description='Reconnect to the server(s) on disconnect',
		default=True
	)

	# input
	device = StringField(
		'Device',
		description='OSS DSP soundcard device for the audio input',
		default='/dev/dsp',
		validators=[DataRequired()]
	)
	sampleRate = SelectField(
		'Sample Rate',
		description='Sampling rate. 22050 is the RR Standard',
		default=44100,
		choices=[(11025, 'Low (11 kHz)'), (22050, 'Medium (22kHz)'), (44100, 'Normal (44kHz)'), (48000, 'High (48kHz)')],
		coerce=int
	)
	bitsPerSample = SelectField(
		'Sample Size',
		description='Bits per sample. 16 for mono feeds, 32 for stereo feeds',
		default=24,
		choices=[(16, 'Low (16 bit)'), (24, 'Normal (24 bit)'), (32, 'High (32 bit)')],
		coerce=int
	)
	channel = SelectField(
		'Channel',
		description='Number of channels. 1=mono, 2=stereo',
		default=2,
		choices=[(1, 'Mono'), (2, 'Stereo')],
		coerce=int
	)

	# icecast2-0
	format = SelectField(
		'Format',
		description='Format  of  the  stream  sent  to the IceCast2 server.',
		default='opus',
		choices=[('opus', 'Opus'), ('mp3', 'MP3'), ('mp2', 'MP2'), ('vorbis', 'OGG Vorbis'), ('aac', 'AAC'), ('aacp', 'AACP')]
	)

	bitrateMode = SelectField(
		'Bitrate Mode',
		description='The bit rate mode of the encoding.',
		default='vbr',
		choices=[('vbr', 'Variable bitrate'), ('cbr', 'Constant bitrate'), ('abr', 'Average bitrate')]
	)

	bitrate = IntegerField(
		'Bitrate',
		description='Bit rate to encode to in kbps (e.g. 96). Only used when cbr or abr bit rate modes are specified.',
		default=320,
		validators=[DataRequired()]
	)

	quality = DecimalField(
		'Quality',
		description='The quality of encoding a value between 0.0 and 1.0 (e.g. 0.8), with 1.0 beeing the highest quality. Use a value greater than 0.0. Only used when vbr bit rate mode is specified for Ogg Vorbis format, or in vbr and abr modes for mp3 and mp2 format.',
		default=0.8,
		places=1,
		validators=[DataRequired(), NumberRange(0., 1., 'Quality setting must be between 0.0 and 1.0')]
	)

	server = StringField(
		'Server',
		description='The IceCast2 server\'s name (e.g. yp.yourserver.com)',
		default='yp.yourserver.com',
		validators=[DataRequired()]
	)

	port = IntegerField(
		'Port',
		description='The port to connect to the IceCast server (e.g. 8000)',
		default=8000,
		validators=[DataRequired(), NumberRange(1, 65535, 'Port outside valid range of 1 to 65535')]
	)

	password = StringField(
		'Password',
		description='The password to use to connect to the IceCast2 server',
		default='MyPassword',
		validators=[DataRequired()]
	)

	mountPoint = StringField(
		'Mount Point',
		description='Mount point for the stream on the server',
		default='stream',
		validators=[DataRequired()]
	)

	configfile_path = StringField(
		'Config file path',
		description='File path of the generated configuration file.',
		default='darkice.conf',
		validators=[DataRequired()]
	)