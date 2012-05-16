from distutils.core import setup

with open('README') as file:
    long_description = file.read()

# There's still some work to do:
# - Work in the platform specific files handling (the cron job)
	
setup(name='pylogan',
	version = '0.3.2',
	author = 'Irving Leonard',
	author_email = 'irvingleonard@ymail.com',
	url = 'https://github.com/irvingleonard/pylogan',
	description = 'Modular Log Analayzer',
	long_description = long_description,
	download_url = 'https://github.com/downloads/irvingleonard/pylogan/pylogan-0.3.2.zip',
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Environment :: Console',
		'Intended Audience :: Developers',
		'Intended Audience :: System Administrators',
		'License :: OSI Approved :: BSD License',
		'Natural Language :: Spanish',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3',
		'Topic :: Communications',
		'Topic :: Internet :: Log Analysis',
		'Topic :: System :: Logging',
		'Topic :: System :: Monitoring',
		'Topic :: System :: Systems Administration',
		],
	provides=['pylogan'],
	requires=['sys','os','os.path','datetime','re','socket','collections','xml.dom.minidom',],
	package_dir = {'pylogan': 'bin/pylogan'},
	packages=['pylogan','pylogan.input','pylogan.process','pylogan.output'],
	scripts=['bin/logan.py',],
	package_data={'pylogan.output': ['themes/*']},
	data_files=[
		('doc/pylogan', ['README',]),
		('doc/pylogan', ['changelog',]),
		('doc/pylogan/cron.d', ['cron.d/pylogan',]),
		]
     )
