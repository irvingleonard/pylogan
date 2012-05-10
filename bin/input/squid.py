
import re

class SquidLine:
	
	def __init__(self, content):
		format = r'^\s*(?P<source_address>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+-\s+(?P<user>\S+)\s+(?P<timestamp>\[\S+\s+\S+])\s+"(?P<method>\S+)\s+(?P<url>\S+)\s+(?P<protocol>\S+)"\s+(?P<answer>\d+)\s+(?P<size>\d+)\s+(?P<squid_request>\S+):(?P<squid_action>\S+)$'
		result = re.match(format, content)
		if result:
			self.source_address = result.group('source_address')
			self.user = result.group('user')
			self.timestamp = result.group('timestamp')
			self.method = result.group('method')
			self.url = result.group('url')
			self.protocol = result.group('protocol')
			self.answer = result.group('answer')
			self.size = result.group('size')
			self.squid_request = result.group('squid_request')
			self.squid_action = result.group('squid_action')
