from distutils.core import setup

with open('README') as file:
    long_description = file.read()

# There's still some work to do;
# - Check the classifiers
# - Get the GitHub repo URL
# - Make a release in github and use the URL
# - Check platforms parameter
# - Check license parameter
# - Work in the platform specific files handling (the cron job)
	
setup(name='pylogan',
	version = '0.3.2',
	author = 'Irving Leonard',
	author_email = 'irvingleonard@ymail.com',
	url = 'TODO',
	description = 'Modular Log Analayzer',
	long_description = long_description,
	download_url = 'TODO',
	classifiers=[
		'Development Status :: 2 - Pre-Alpha',
		'Environment :: Console',
		'Intended Audience :: Developers',
		'Intended Audience :: System Administrators',
		'License :: OSI Approved :: BSD License',
		'Operating System :: ANY',
		'Programming Language :: Python',
		'Topic :: Communications',
		'Topic :: Internet :: Log Analysis',
		'Topic :: System :: Logging',
		'Topic :: System :: Monitoring',
		'Topic :: System :: Systems Administration',
		],
	platforms=['ANY'],
	license='BSD',
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
