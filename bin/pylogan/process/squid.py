
import re
import socket

class Use:
	"""Get usage statistics from syslog lines.
	"""
	
	def __init__(self, source):
		self.source = source
	
	def filter(self, line):
		"""Checks if a request actually creates traffic
		
		There's a possibility of "not authorized" or "cache hit"
		"""
		
		if line.content.squid_action == 'DIRECT':
			return True
		else:
			return False
	
	def by_users(self):
		"""Get traffic totals grouped by users.
		"""
		
		users = {}
		for line in self.source.lines:
			try:
				if self.filter(line):
					if line.content.user not in users.keys():
						users[line.content.user] = 0
					users[line.content.user] += int(line.content.size)
			except AttributeError:
				pass
		
		# TODO: sort; convert to lists is even better
			
		return users
		
	def by_domains(self):
		"""Get traffic totals grouped by domains.
		"""
		
		# TODO: use urllib instead
		url_format = r'^\s*(?:(?P<protocol>\w+)://)?(?P<domain>[\w\d\-\.]+)(?::(?P<port>\d+))?/?(?P<everything_else>.*)$'
		sites = {}
		for line in self.source.lines:
			try:
				if self.filter(line):
					result = re.match(url_format, line.content.url)
					if result.group('domain') not in sites.keys():
						sites[result.group('domain')] = 0
					sites[result.group('domain')] += int(line.content.size)
			except AttributeError:
				pass
		
		# TODO: sort; convert to lists is even better
		
		return sites
		
	def by_navigations(self):
		"""Get traffic totals grouped by navigations.
		
		A navigation is an interception of a user in a host generating traffic for a domain.
		"""
		
		url_format = r'^\s*(?:(?P<protocol>\w+)://)?(?P<domain>[\w\d\-\.]+)(?::(?P<port>\d+))?/?(?P<everything_else>.*)$'
		navigations = {}
		for line in self.source.lines:
			try:
				if self.filter(line):
					result = re.match(url_format, line.content.url)
					if line.content.source_address not in navigations.keys():
						navigations[line.content.source_address] = {}
					if line.content.user not in navigations[line.content.source_address]:
						navigations[line.content.source_address][line.content.user] = {}
					if result.group('domain') not in navigations[line.content.source_address][line.content.user]:
						navigations[line.content.source_address][line.content.user][result.group('domain')] = 0
					navigations[line.content.source_address][line.content.user][result.group('domain')] += int(line.content.size)
			except AttributeError:
				pass
		
		flat_navigations = []
		for address in navigations.keys():
			# node = socket.getfqdn(address)
			node = address
			for user in navigations[address].keys():
				for domain in navigations[address][user].keys():
					flat_navigations.append([user, domain, node, address, navigations[address][user][domain]])
		
		# What happend here? Why an exception handler is needed?
		try:
			flat_navigations.sort(key = lambda t: t[4], reverse = True)
		except (e):
			pass
		
		return flat_navigations
