
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
	
	def out(self, dates, users, domains, navigations):
		users = collections.OrderedDict(sorted(users.items(), key=lambda t: t[1], reverse = True))
		domains = collections.OrderedDict(sorted(domains.items(), key=lambda t: t[1], reverse = True))
		
		top_users = list(users.keys())[:10]
		top_domains = list(domains.keys())[:10]
		
		dates = list(dates)
		
		the_dom = xml.dom.minidom.parse(self.theme_path)
		
		h2s = the_dom.documentElement.lastChild.getElementsByTagName('h2')
		for i in range(h2s.length):
			if h2s.item(i).getAttribute('id') == 'time_span':
				date_difference = dates[1] - dates[0]
				try:
					if date_difference.days == 0:
						h2s.item(i).appendChild(the_dom.createTextNode('(' + dates[0].strftime('%I:%M%p') + " - " + dates[1].strftime('%I:%M%p') + ")"))
					elif date_difference.days < 28:
						h2s.item(i).appendChild(the_dom.createTextNode('(' + dates[0].strftime('%d %I:%M%p') + " - " + dates[1].strftime('%d %I:%M%p') + ")"))
					elif date_difference.days < 365:
						h2s.item(i).appendChild(the_dom.createTextNode('(' + dates[0].strftime('%m/%d %I:%M%p') + " - " + dates[1].strftime('%m/%d %I:%M%p') + ")"))
					else:
						h2s.item(i).appendChild(the_dom.createTextNode('(' + dates[0].strftime('%Y/%m/%d %I:%M%p') + " - " + dates[1].strftime('%Y/%m/%d %I:%M%p') + ")"))
				except AttributeError:
					pass
		divs = the_dom.documentElement.lastChild.getElementsByTagName('div')
		for i in range(divs.length):
			if divs.item(i).getAttribute('id') == 'users':
				for user in top_users:
					row = the_dom.createElement('tr')
					divs.item(i).getElementsByTagName('table').item(0).appendChild(row)
					name = the_dom.createElement('td')
					row.appendChild(name)
					name.setAttribute('class','property')
					name.appendChild(the_dom.createTextNode(user))
					value = the_dom.createElement('td')
					row.appendChild(value)
					value.setAttribute('class','size')
					value.appendChild(the_dom.createTextNode(readeable_size(users[user])))
					
			elif divs.item(i).getAttribute('id') == 'domains':
				for domain in top_domains:
					row = the_dom.createElement('tr')
					divs.item(i).getElementsByTagName('table').item(0).appendChild(row)
					name = the_dom.createElement('td')
					row.appendChild(name)
					name.setAttribute('class','property')
					name.appendChild(the_dom.createTextNode(domain))
					value = the_dom.createElement('td')
					row.appendChild(value)
					value.setAttribute('class','size')
					value.appendChild(the_dom.createTextNode(readeable_size(domains[domain])))
			elif divs.item(i).getAttribute('id') == 'navigations':
				for navigation in navigations[:10]:
					row = the_dom.createElement('tr')
					divs.item(i).getElementsByTagName('table').item(0).appendChild(row)
					for data in navigation:
						element = the_dom.createElement('td')
						row.appendChild(element)
						element.appendChild(the_dom.createTextNode(str(data)))
					element.replaceChild(the_dom.createTextNode(readeable_size(navigation[-1])), element.firstChild)
					element.setAttribute('class', 'size')
		
		index = open(self.output_path, mode = 'w', encoding = 'utf-8')
		the_dom.writexml(index)
		index.close()
