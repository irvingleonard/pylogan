
class loganException(Exception):
  pass

import sys
import os
import os.path
import datetime
import input.syslog
import process.squid
import output.html

os.chdir(os.path.dirname(sys.argv[0]))

lock_path = os.path.abspath(os.path.join('/', 'var', 'lock', 'pylogan.lock'))
if os.path.isfile(lock_path):
	with open(lock_path) as file:
		print('According to the lock file pylogan is still running with PID ', file.readline())
	sys.exit()

lock = open(lock_path, 'w')
lock.write(str(os.getpid()))
lock.close()

messages_path = os.path.abspath(os.path.join('/', 'var', 'log', 'messages'))

messages = input.syslog.SyslogFile(path = messages_path, filters = {'process': ["squid"], 'start_date': datetime.datetime.combine(datetime.date.today(), datetime.time())})
processor = process.squid.Use(messages)

out = output.html.SquidResume()
out.out((messages.start_date, messages.last_date), processor.by_users(), processor.by_domains(), processor.by_navigations())

os.unlink(lock_path)
