
import re
import datetime

import pylogan.input.squid

#TODO: Research about no process lines (switch lines), and make a really universal syslog regexp
syslog_format = r'^(\w+\s+\d+\s+\d+:\d+:\d+)\s+([\w\d\.]+)\s+([\w/]+)\[(\d+)\]:(.*)$'

class SyslogException(Exception):
	"""Module base exception
	"""
	pass

class SyslogInputError(SyslogException):
  """Error in file input
  """
  pass

class SyslogParseError(SyslogException):
  """Error parsing the line
  """
  pass

class SyslogLine:
	"""Structural class for every line

	It happend to be a struct to accomodate a line data after exploding the string
	"""
	
	def __init__(self, line, formats = [re.compile(syslog_format)], year = None):
		
		# Syslog doesn't print the year in it lines
		if not year:
			year = datetime.datetime.now().year
			
		if self._parse(line, formats):
			# Time data handling
			self.date = datetime.datetime.strptime(str(year) + " " + self.time_stuff, '%Y %b %d %H:%M:%S')
			del(self.time_stuff)
			
			#TODO: Implement the message type detection and mining logic.
			self.content = pylogan.input.squid.SquidLine(self.message)
			del(self.message)
		else:
			raise SyslogParseError("Line not parsed: " + line)
	
	def _parse(self, line, formats):
		"""Actual line parsing
		
		Just the syslog part of the line
		"""
		
		for format in formats:
			result = re.match(format,line)
			#TODO: Use named grouping
			if result:
				self.time_stuff = result.group(1)
				self.host = result.group(2)
				self.process = result.group(3)
				self.pid = result.group(4)
				self.message = result.group(5)
				return True
		return False

class SyslogFile:
	"""Structural class for a syslog file

	Some procedures to get a file content
	"""

	def __init__(self, path = "messages", filters = None, load = True):
		self.path = path
		self.lines = []
		self.filters = filters
		self.start_date = None
		self.last_date = None
		if load:
			self._load()
	
	def _load(self):
		"""File parsing
		
		Read every line in the file to memory, posibly filtered
		"""
		try:
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
		except IOError as err:
			try:
				if err.filename == self.path:
					raise SyslogInputError("Error with file " + err.filename + " check existence and permissions")
				else:
					raise SyslogInputError(err)
			except IOError as todoerr:
				print("TODO", todoerr)
			
			
	def filter(self, line):
		"""Filter a line
		
		Filter some lines from the very populated syslog file
		Actually only implemented the "process" and "start_date" filters.
		"""
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
