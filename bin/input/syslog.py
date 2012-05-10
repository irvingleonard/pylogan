
syslog_format = r'^(\w+\s+\d+\s+\d+:\d+:\d+)\s+([\w\d\.]+)\s+([\w/]+)\[(\d+)\]:(.*)$'

import re
import datetime

import input.squid as squid

class SyslogException(Exception):
	pass

class SyslogInputError(SyslogException):
  """Error in line
  """
  pass

class SyslogParseError(SyslogException):
  """
  """
  pass

class SyslogLine:
	"""Structural class for every line

	It happend to be a struct to accomodate a line data after exploding the string
	"""
	
	def __init__(self, line, formats = [re.compile(syslog_format)], year = None):
		if not year:
			year = datetime.datetime.now().year
		if self._parse(line, formats):
			self.date = datetime.datetime.strptime(str(year) + " " + self.time_stuff, '%Y %b %d %H:%M:%S')
			del(self.time_stuff)
			self.content = squid.SquidLine(self.message)
			del(self.message)
		else:
			raise SyslogParseError("Line not parsed: " + line)
		# line_timestamp=time.mktime(time.strptime('%d %s' % (_year, line_result.group(1)),'%Y %b %d %H:%M:%S'))
		# self.timestamp = line_timestamp
		# self.host = src_host
		# self.data = process_data
	
	def _parse(self, line, formats):
		for format in formats:
			result = re.match(format,line)
			if result:
				self.time_stuff = result.group(1)
				self.host = result.group(2)
				self.process = result.group(3)
				self.pid = result.group(4)
				self.message = result.group(5)
				return True
		return False

class SyslogFile:

	def __init__(self, path = "messages", filters = None, load = True):
		self.path = path
		self.lines = []
		self.filters = filters
		self.start_date = None
		self.last_date = None
		if load:
			self._load()
	
	def _load(self):
		with open(self.path) as file:
			for line in file:
				try:
					line_result = SyslogLine(line)
				except SyslogParseError:
					pass	#do logging (TODO)
				else:
					if self.filter(line_result):
						if not self.start_date:
							self.start_date = line_result.date
						self.lines.append(line_result)
						self.last_date = line_result.date
		
	def filter(self, line):
		valid = True
		if 'process' in self.filters.keys():
			process_ok = False
			for process in self.filters['process']:
				if line.process == process:
					process_ok = True
			valid = valid and process_ok
		if 'start_date' in self.filters.keys():
			if line.date < self.filters['start_date']:
				valid = False
				
		return valid
