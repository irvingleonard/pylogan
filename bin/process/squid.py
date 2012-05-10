
import re

class Use:
	
	def __init__(self, source):
		self.source = source
	
	def by_users(self):
		users = {}
		for line in self.source.lines:
			try:
				if line.content.user not in users.keys():
					users[line.content.user] = 0
				users[line.content.user] += int(line.content.size)
			except AttributeError:
				pass
		
		# TODO sort and limit
			
		return users
		
	def by_domains(self):
		url_format = r'^\s*(?:(?P<protocol>\w+)://)?(?P<domain>[\w\d\-\.]+)(?::(?P<port>\d+))?/?(?P<everything_else>.*)$'
		sites = {}
		for line in self.source.lines:
			try:
				result = re.match(url_format, line.content.url)
				if result.group('domain') not in sites.keys():
					sites[result.group('domain')] = 0
				sites[result.group('domain')] += int(line.content.size)
			except AttributeError:
				pass
		return sites