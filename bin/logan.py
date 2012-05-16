#!/usr/bin/python
# -*- coding: utf-8 -*-

class loganException(Exception):
  pass

import sys
import os
import os.path
import datetime

import pylogan.input.syslog
import pylogan.process.squid
import pylogan.output.html

#Set working enviroment
os.chdir(os.path.dirname(sys.argv[0]))

#Only one logan instance is allowed to run, setting lock
# TODO: Does a locking module exists? What about windows?
lock_path = os.path.abspath(os.path.join('/', 'var', 'lock', 'pylogan.lock'))
if os.path.isfile(lock_path):
	with open(lock_path) as file:
		if os.getpid() == file.readline():
			print('pylogan is still running with PID ', file.readline())
			file.close()
			sys.exit()
		else:
			print('pylogan was running with PID ', file.readline(), " the current PID is ", os.getpid())
			file.close()
			os.unlink(lock_path)
try:
	lock = open(lock_path, 'w')
	lock.write(str(os.getpid()))
	lock.close()
except IOError as err:
	print("Error locking: " + str(err))
	sys.exit()

#TODO: There's no config file, it should be somewhere then
messages_path = os.path.abspath(os.path.join('/', 'var', 'log', 'messages'))
output_path = os.path.abspath('.')
# output_path = os.path.abspath(os.path.join('/', 'srv', 'www', 'htdocs'))

#There's no logic in here at all, this is just what's needed to show a squid resume in html, the first thing that was implemented.
#TODO: Implement the script logic
try:
	messages = pylogan.input.syslog.SyslogFile(path = messages_path, filters = {'process': ["squid"], 'start_date': datetime.datetime.combine(datetime.date.today(), datetime.time())})
except pylogan.input.syslog.SyslogInputError as err:
	print(err)
else:
	processor = pylogan.process.squid.Use(messages)
	out = pylogan.output.html.SquidResume(output_path = output_path)
	out.out((messages.start_date, messages.last_date), processor.by_users(), processor.by_domains(), processor.by_navigations())
finally:
	os.unlink(lock_path)
