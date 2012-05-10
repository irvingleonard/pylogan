
class loganException(Exception):
  pass

import sys
import os
import os.path
import input.syslog
import process.squid
import output.html


# import datetime
# line = 'May  2 12:36:49 proxy squid[22801]: 192.168.18.150 - neyder [02/May/2012:12:36:49 -0400] "GET http://proxy.ccron.cu/acceso_denegado.html HTTP/1.0" 200 1653 TCP_CLIENT_REFRESH_MISS:DIRECT'
# testing = input.syslog.SyslogLine(line)
# testing = datetime.datetime.strptime("2012 May  2 12:36:49", '%Y %b %d %H:%M:%S')
# print("Host", test.host, sep = " : ")
# print("Date", test.date, sep = " : ")
# print("Process", test.process, sep = " : ")
# print("PID", test.pid, sep = " : ")
# print("Message", test.message, sep = " : ")

os.chdir(os.path.dirname(sys.argv[0]))

messages_path = os.path.abspath(os.path.join('/', 'var', 'log', 'messages'))
messages_path = os.path.abspath(os.path.join('..', 'messages'))

messages = input.syslog.SyslogFile(path = messages_path, filter = "squid")
processor = process.squid.Use(messages)

out = output.html.SquidResume()
out.out(processor.by_users(), processor.by_domains())
