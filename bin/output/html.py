
import os.path
import collections
import xml.dom.minidom

def readeable_size(size):
	multiplier = 1
	while size >= 1024:
		size = size / 1024
		multiplier *= 1024
	
	size = str(round(size, 2))
	if multiplier == 1024 ** 0:
		size += ""
	elif multiplier == 1024 ** 1:
		size += "K"
	elif multiplier == 1024 ** 2:
		size += "M"
	elif multiplier == 1024 ** 3:
		size += "G"
	elif multiplier == 1024 ** 4:
		size += "T"
	
	size += "B"
	return size

class SquidResume:
	
	def __init__(self):
		self.theme_path = os.path.abspath(os.path.join("..","themes","simple.xhtml"))
		self.output_path = os.path.abspath(os.path.join("..","webroot","index.xhtml"))
	
	def out(self, users, domains):
		users = collections.OrderedDict(sorted(users.items(), key=lambda t: t[1], reverse = True))
		domains = collections.OrderedDict(sorted(domains.items(), key=lambda t: t[1], reverse = True))
		
		top_users = list(users.keys())[:10]
		top_domains = list(domains.keys())[:10]
		
		the_dom = xml.dom.minidom.parse(self.theme_path)
		
		divs = the_dom.documentElement.lastChild.getElementsByTagName('div')
		for i in range(divs.length):
			if divs.item(i).getAttribute('id') == 'users':
				for user in top_users:
					row = the_dom.createElement('tr')
					divs.item(i).appendChild(row)
					name = the_dom.createElement('td')
					row.appendChild(name)
					name.setAttribute('class','property')
					name.appendChild(the_dom.createTextNode(user))
					value = the_dom.createElement('td')
					row.appendChild(value)
					value.setAttribute('class','value')
					value.appendChild(the_dom.createTextNode(readeable_size(users[user])))
					
			elif divs.item(i).getAttribute('id') == 'domains':
				for domain in top_domains:
					row = the_dom.createElement('tr')
					divs.item(i).appendChild(row)
					name = the_dom.createElement('td')
					row.appendChild(name)
					name.setAttribute('class','property')
					name.appendChild(the_dom.createTextNode(domain))
					value = the_dom.createElement('td')
					row.appendChild(value)
					value.setAttribute('class','value')
					value.appendChild(the_dom.createTextNode(readeable_size(domains[domain])))
				
		
		index = open(self.output_path, mode = 'w', encoding = 'utf-8')
		the_dom.writexml(index)
		# print(self.theme_path, self.output_path, sep=" - ")
		
	